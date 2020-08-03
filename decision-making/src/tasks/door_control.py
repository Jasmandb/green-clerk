from src.app_config import States, Pins, Arduino, logging
from nanpy import ArduinoApi, SerialManager, DoorCont

logger = logging.getLogger(__name__)


class DoorControl:
    def __init__(self):
        self.ard_api = None
        self.door_control = None
        self.ard_id = Arduino.ard_3
        self.connection = None

    def run(self, state):
        self.create_connection_channel()
        self.setup_door_control_obj()
        if state == States.OPEN:
            logger.debug('Opening the door requested state is {}'.format(state))
            self.door_control.open_door()
        else:
            logger.debug('Closing the door requested state is state {}'.format(state))
            self.door_control.close_door()
        self.close_ard_connection()

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            self.connection = SerialManager(device=self.ard_id)
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logging.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def setup_door_control_obj(self):
        self.door_control = DoorCont(Pins.DOOR[0], Pins.DOOR[1], Pins.DOOR[2], self.connection)

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
