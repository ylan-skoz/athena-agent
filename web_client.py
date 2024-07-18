import asyncio
import websockets
from time import sleep
import json
from agent_logger import setup_logger


logger = setup_logger('socket_logger', 'agent.log')

class WebClient:
    def __init__(self, server_url, device_id, api_key):
        self.server_url = server_url
        self.device_id = device_id
        self.api_key = api_key
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.server_url)
            logger.info(f"Connected to server: {self.server_url}")
            await self.authenticate()
        except Exception as e:
            logger.error(f"Failed to connect to server: {e}")

    async def authenticate(self):
        auth_message = {
            "type": "auth",
            "device_id": self.device_id,
            "api_key": self.api_key
        }
        await self.send(auth_message)

    async def send(self, message):
        if self.websocket:
            payload=json.dumps(message)
            await self.websocket.send(payload)

            logger.info(f"Sent message: {message}")
        else:
            logger.error("Can't send message, websocket connection not established")

    async def receive(self):
        if self.websocket:
            try:
                message = await self.websocket.recv()
                logger.info(f"Received message: {message}")
                return message
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket connection closed")
                await self.reconnect()
        else:
            logger.error("Can't receive message, websocket connection not established")
            sleep(1)

    async def reconnect(self):
        logger.info("Attempting to reconnect...")
        await self.connect()

    async def run(self):
        await self.connect()

        while True:
            try:
                message = await self.receive()
                # Process the received message here
            except Exception as e:
                logger.error(f"Error in run loop: {e}")
                await asyncio.sleep(5)  # Wait before attempting to reconnect

    def start(self):
        asyncio.run(self.run())

# Example usage:
# client = WebClient("wss://example.com/ws", "device123", "api_key_here")
# client.start()