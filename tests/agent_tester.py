import asyncio
import websockets
import json
import random
import socket
import ipaddress
from message_structure import MESSAGE_STRUCTURE
from agent_logger import setup_logger

# Set up custom logger
logger = setup_logger('client_logger', 'client.log')

# Define a range of ports to scan
PORT_RANGE = range(8000, 9000)  # Adjust this range as needed

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((str(ip), port))
    sock.close()
    return result == 0

async def find_server():
    local_ip = get_local_ip()
    
    for port in PORT_RANGE:
        if scan_port(local_ip, port):
            logger.info(f"Potential server found at {local_ip}:{port}")
            if await verify_websocket_server(local_ip, port):
                logger.info(f"WebSocket server confirmed at {local_ip}:{port}")
                return local_ip, port
    
    logger.error("Server not found on the local network")
    return None, None

async def verify_websocket_server(ip, port):
    uri = f"ws://{ip}:{port}"
    try:
        async with websockets.connect(uri, timeout=1) as websocket:
            # You might want to implement a specific handshake here
            return True
    except:
        return False

async def send_test_data(server_ip, server_port):
    uri = f"ws://{server_ip}:{server_port}"
    logger.info(f"Attempting to connect to {uri}")

    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to WebSocket server")
            
            for i in range(5):  # Send 5 test messages
                test_data = {
                    MESSAGE_STRUCTURE.ID: i,
                    MESSAGE_STRUCTURE.TYPE.NAME: MESSAGE_STRUCTURE.TYPE.TELEMETRY,
                    "timestamp": asyncio.get_event_loop().time(),
                    "data": {
                        "temperature": round(random.uniform(20.0, 30.0), 2),
                        "humidity": round(random.uniform(40.0, 60.0), 2)
                    }
                }
                
                await websocket.send(json.dumps(test_data))
                logger.info(f"Sent: {test_data}")
                
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    logger.info(f"Received: {response}")
                except asyncio.TimeoutError:
                    logger.warning("No response received within timeout.")
                
                await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosedError as e:
        logger.error(f"WebSocket connection closed unexpectedly: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

async def main():
    server_ip, server_port = await find_server()
    if server_ip and server_port:
        await send_test_data(server_ip, server_port)
    else:
        logger.error("Could not find the server. Make sure it's running and on the same network.")

if __name__ == "__main__":
    asyncio.run(main())