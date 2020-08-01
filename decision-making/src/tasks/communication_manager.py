from src.app_config import logging

from nanpy import SerialManager, ArduinoApi

logger = logging.getLogger(__name__)


class CommunicationManager:
    def __init__(self, ard_id):
        self.ard_api = None
        self.ard_id = ard_id
        self.connection = None
        self.create_connection_channel()

    def create_connection_channel(self):
        try:
            self.connection = SerialManager(device=self.ard_id)
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logger.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def close_ard_connection(self):
        self.connection.close()


if __name__ == '__main__':
    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager('/dev/ttyUSB0')
    logger.debug('closing the arduino connection')
    communication_manager.close_ard_connection()
