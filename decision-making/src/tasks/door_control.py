from src.app_config import States, Pins, Arduino, logging
from nanpy import ArduinoApi, SerialManager, Relay

logger = logging.getLogger(__name__)


class DoorControl:
    def __init__(self):
        self.ard_api = None
        self.relay = None
        self.ard_id = Arduino.ard_3
        self.connection = None

    def run(self, state):
        self.create_connection_channel()
        self.setup_relay_obj()
        if state == States.OPEN:
            logger.debug('Opening the door requested state is {}'.format(state))
            # self.ard_api.digitalWrite(Pins.RELAY_PINS[0], self.ard_api.LOW)
            self.relay.open()
        else:
            logger.debug('Closing the door requested state is state {}'.format(state))
            # self.ard_api.digitalWrite(Pins.RELAY_PINS[0], self.ard_api.HIGH)
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
        pass

    def close_ard_connection(self):
        self.connection.close()


if __name__ == '__main__':
    logger.info('DoorControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            DoorControl().run(States.OPEN)
        else:
            DoorControl().run(States.CLOSE)
