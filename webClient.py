import asyncio
import websockets
from agent_logger import setup_logger

logger = setup_logger('socket_logger', 'agent.log')

class WebClient():

    def __init__(self, serverUrl):
        self.serverUrl = serverUrl

    async def _connect_to_server(self):
            try:
                async with websockets.connect(self.serverUrl) as websocket:
                    logger.info(f"Connected to server at {self.serverUrl}")
                    while True:
                        message = await websocket.recv()
                        logger.info(f"Received message from server: {message}")
                        self.message_queue.put(message)
            except Exception as e:
                logger.error(f"Failed to connect to server at {self.serverUrl}: {e}")

    def start_server_connection(self):
        asyncio.run(self._connect_to_server())