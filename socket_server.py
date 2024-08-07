import asyncio
import websockets
import json
import socket
from queue import Queue
from datetime import datetime
from time import time
from agent_logger import setup_logger
from message_structure import MESSAGE_STRUCTURE

# Set up custom logger
logger = setup_logger('server_logger', 'agent.log')


class SocketServer:


    # This will store our connected clients
    clients = {}
    upstream_message_queue: Queue

    def __init__(self, upstream_message_queue):
        self.upstream_message_queue = upstream_message_queue

    async def handle_client(self, websocket, path):
        
        # Wait for client identification
        client_id = str(id(websocket))
        logger.info(f"Client {client_id} connected")
       
        # Register the client
        self.clients[client_id] = websocket
        try:
            async for message in websocket:
                data = json.loads(message)
                logger.info(f"Received data from {client_id}: {data} in handle_client")

                self.upstream_message_queue.put(data)

                acknowledge = {
                    MESSAGE_STRUCTURE.TYPE.NAME: MESSAGE_STRUCTURE.TYPE.ACKNOWLEDGE,
                    # MESSAGE_STRUCTURE.ID: data[MESSAGE_STRUCTURE.ID],
                    MESSAGE_STRUCTURE.ACKNOWLEDGE.STATUS.NAME: MESSAGE_STRUCTURE.ACKNOWLEDGE.STATUS.RECEIVED
                    }
                await self.clients[client_id].send(json.dumps(acknowledge))
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from client {client_id}")
        except Exception as e:
            logger.exception(f"Error when handling client {client_id}: {str(e)}")
        finally:
            # Unregister the client
            if client_id in self.clients:
                del self.clients[client_id]
                logger.info(f"Client {client_id} has been unregistered")

    # Broadcast message to all connected clients
    async def broadcast(self, message):
        # Send a message to all connected clients
        if self.clients:
            await asyncio.gather(*[self.clients[key].send(message) for key in self.clients.keys()])

    def _get_ip(self):
        # Get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    async def initiate_socket_server(self):
        ip = self._get_ip()

        port_range = (8000, 9000)


        for port in range (port_range[0], port_range[1]):
            try:
                server = await websockets.serve(self.handle_client, ip, port)
                break
            except OSError:
                continue
        else:
            logger.error (f"No available port was found in range {port_range}")
        # Get the assigned port
        port = server.sockets[0].getsockname()[1]
        
        logger.info(f"WebSocket server started on ws://{ip}:{port}")
        
        # Optional: If you want to save the port to a file for other processes to read
        with open('server_port.txt', 'w') as f:
            f.write(str(port))
        
        await server.wait_closed()