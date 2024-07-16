import asyncio
from queue import Queue, Empty
from threading import Thread
from socket_server import SocketServer
from time import time, sleep
from datetime import datetime
from agent_logger import setup_logger
from web_client import WebClient
from time import sleep
from message_structure import MESSAGE_STRUCTURE

from dotenv import load_dotenv
import os

load_dotenv()  # This line brings all environment variables from .env into os.environ

logger = setup_logger('socket_logger', 'agent.log')

class AthenaAgent:
    def __init__(self) -> None:
        self.message_queue = Queue()
        self.server = SocketServer(self.message_queue)
        self.socket_server_thread = Thread(target=self._run_socket_server, daemon=True)
        self.message_processing_threads = Thread(target=self._process_queue, daemon=True)
        
        self.message_process_interval = 5
        self.batch_size = 50

        # Webclient
        self.serverUrl = "ws://192.168.1.23:8085"
        self.device_id = os.environ['DEVICE_ID']
        self.api_key = os.environ['API_KEY']
        self.webClient = WebClient(server_url=self.serverUrl, device_id=self.device_id, api_key=self.api_key)
        self.web_client_thread = Thread(target=self.webClient.start, daemon=True)


    def _run_socket_server(self):
        asyncio.run(self.server.initiate_socket_server())

######################################################################
################# Incoming client messages management ################
######################################################################

    def _process_queue(self):
        while True:
            batch = []
            start_time = time()
            
            # Collect messages into a batch until the batch size is reached or the interval time has passed
            while len(batch) < self.batch_size and time() - start_time < self.message_process_interval:
                try:
                    message = self.message_queue.get(timeout=1)
                    batch.append(message)
                except Empty:
                    # Continue waiting if the queue is empty
                    continue

            # Process the batch if it contains any messages
            if batch:
                self._process_batch(batch)

            # Sleep to maintain a consistent processing interval, adjusting for processing time
            elapsed_time = time() - start_time
            sleep_time = max(0, self.message_process_interval - elapsed_time)
            sleep(sleep_time)

    def _process_batch(self, batch):

        telemetry_list = []
        notification_list = []
        for message in batch:
            if 'telemetry' in message:
                telemetry_list.append(message['telemetry'])
            elif 'notification' in message:
                notification_list.append(message['notification'])


        formated_batch = {
            MESSAGE_STRUCTURE.TYPE.NAME: MESSAGE_STRUCTURE.TYPE.DATA,
            MESSAGE_STRUCTURE.DEVICE_ID: self.device_id,
            'payload':
            {
                'telemetry': telemetry_list,
                'notification': notification_list
            }
        }

        asyncio.run(self.webClient.send(formated_batch))
        # Example: for message in batch: process(message)


    def send_messages_to_clients(self, message):
        if isinstance(message, str):
            asyncio.run(self.server.broadcast(message))

    def start(self):
        self.socket_server_thread.start()
        self.message_processing_threads.start()
        self.web_client_thread.start()

if __name__ == "__main__":
    agent = AthenaAgent()
    agent.start()

while True:
    sleep(5)