from src.app_config import States, Pins, logging
from nanpy import DoorCont

logger = logging.getLogger(__name__)


class DoorControl:
    def __init__(self, connection):
        self.door_control = None
        self.connection = connection

    def run(self, state):
        self.setup_door_control_obj()
        if state == States.OPEN:
            logger.debug('Opening the door requested state is {}'.format(state))
            self.door_control.open_door()
        else:
            logger.debug('Closing the door requested state is state {}'.format(state))
            self.door_control.close_door()

    def setup_door_control_obj(self):
        self.door_control = DoorCont(Pins.DOOR[0], Pins.DOOR[1], Pins.DOOR[2], self.connection)


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager
    from src.app_config import Arduino
    from src.tasks.arduino_manager import ArduinoManager

    logger.debug('starting new arduino connection')
    ard_manager = ArduinoManager()
    ard_manager.run()

    communication_manager = CommunicationManager(Arduino['detect_item'])
    logger.info('DoorControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            DoorControl(communication_manager.connection).run(States.OPEN)
        else:
            DoorControl(communication_manager.connection).run(States.CLOSE)
