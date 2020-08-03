from src.app_config import States, Pins, Arduino, logging
from nanpy import ArduinoApi, SerialManager, Relay

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self):
        self.ard_api = None
        self.relay = None
        self.ard_id = Arduino.ard_3
        self.connection = None

    def run(self, state):
        self.create_connection_channel()
        self.setup_relay_obj()
        logger.debug('The requested state is {}'.format(state))
        if state == States.OPEN:
            self.relay.open()
        else:
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
        # TODO: Since we are not expected to expand our number of relays this class is only coded for one sensor
        # TODO: extend to have the ability to expand (I don't think this is necessary though)
        self.relay = Relay(Pins.RELAY_PINS[0], self.connection)

    def close_ard_connection(self):
        self.connection.close()


if __name__ == '__main__':
    logger.info('RelayControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            RelayControl().run(States.OPEN)
        else:
            RelayControl().run(States.CLOSE)
