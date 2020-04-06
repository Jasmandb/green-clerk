from src.app_config import RelayStates, Pins, Arduino, logging
from nanpy import ArduinoApi, SerialManager

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self):
        self.ard_api = None
        self.ard_id = Arduino.ard_3
        self.connection = None
        self.create_connection_channel()
        self.setup_pin_modes()

    def run(self, state):
        if state == RelayStates.OPEN:
            logger.debug('Opening the lid requested state is {}'.format(state))
            self.ard_api.digitalWrite(Pins.RELAY_PINS[0], self.ard_api.LOW)
        else:
            logger.debug('Closing the lid requested state is state {}'.format(state))
            self.ard_api.digitalWrite(Pins.RELAY_PINS[0], self.ard_api.HIGH)

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            self.connection = SerialManager(device=self.ard_id)
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logging.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def setup_pin_modes(self):
        # TODO: Since we are not expected to expand our number of relays this class is only coded for one sensor
        # TODO: extend to have the ability to expand (I don't think this is necessary though)
        self.ard_api.pinMode(Pins.RELAY_PINS[0], self.ard_api.OUTPUT)

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
