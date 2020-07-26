from src.app_config import RelayStates, Pins, Arduino, logging
from nanpy import ArduinoApi, SerialManager, Relay

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self, pin=None):
        self.ard_api = None
        self.pin = None
        self.relay = None
        self.ard_id = Arduino.ard_3
        self.connection = None

    def run(self, state):
        self.create_connection_channel()
        self.setup_relay_obj()
        if state == RelayStates.OPEN:
            logger.debug('Opening the lid requested state is {}'.format(state))
            self.relay.open()
        else:
            logger.debug('Closing the lid requested state is state {}'.format(state))
            self.relay.close()
        self.close_ard_connection()

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            self.connection = SerialManager(device=self.ard_id)
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logging.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def setup_relay_obj(self):
        self.relay = Relay(self.pin, self.connection)

    def close_ard_connection(self):
        self.connection.close()


if __name__ == '__main__':
    logger.info('RelayControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            RelayControl().run(RelayStates.OPEN)
        else:
            RelayControl().run(RelayStates.CLOSE)
