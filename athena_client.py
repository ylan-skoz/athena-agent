from agent_logger import setup_logger


agent_logger = setup_logger('agent_logger', 'agent.log')


class AthenaAgent:

    def __init__(self):
        pass

    def send_data(self, data, component):

        agent_logger.info(f"Data: [{data}] associated with component {component} was just received.")



