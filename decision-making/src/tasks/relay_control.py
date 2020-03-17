from src.app_config import RelayStates, Pins
from nanpy import ArduinoApi, SerialManager
import logging

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self):
        self.ard_api = None
        self.create_connection_channel()
        self.setup_pin_modes()
        self.ard_id = '/dev/ttyACM1'

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
            self.ard_api = ArduinoApi(connection=SerialManager(device=self.ard_id))
        except Exception as e:
            logging.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def setup_pin_modes(self):
        # TODO: Since we are not expected to expand our number of relays this class is only coded for one sensor
        # TODO: extend to have the ability to expand (I don't think this is necessary though)
        self.ard_api.pinMode(Pins.RELAY_PINS, self.ard_api.OUTPUT)


if __name__ == '__main__':
    logger.info('RelayControl')
    import time

    while True:
        RelayControl().run(RelayStates.OPEN)
        time.sleep(2)
        RelayControl().run(RelayStates.CLOSE)
        time.sleep(2)
