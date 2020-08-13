import time
from src.app_config import Pins, BinLocation, logging
from nanpy import Motor

logger = logging.getLogger(__name__)


class RotateTarget:
    def __init__(self, connection):
        self.servo = None
        self.bin_type = None
        self.connection = connection
        self.setup_motor_obj()

    def setup_motor_obj(self):
        self.servo = Motor(Pins.SERVO_PINS[0], self.connection)
        logger.debug('Motor pin {}'.format(Pins.SERVO_PINS[0]))

    def run(self, bin_type):
        self.bin_type = bin_type
        self.servo.move(int(BinLocation[bin_type]), False)

    def roll_back(self):
        self.servo.move(int(BinLocation[self.bin_type]), True)


if __name__ == '__main__':
    from src.app_config import Classification
    from src.tasks.communication_manager import CommunicationManager
    from src.app_config import Arduino
    from src.tasks.arduino_manager import ArduinoManager

    logger.debug('starting new arduino connection')
    ard_manager = ArduinoManager()
    ard_manager.run()
    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager(Arduino['detect_item'])

    logger.info('RotateTarget')
    test = input('Enter a number: ')
    if test == '1':
        logger.debug(
            'Moving to bin: {}, {} degrees'.format(Classification.GARBAGE, BinLocation[Classification.GARBAGE]))
        rotate_target1 = RotateTarget(communication_manager.connection)
        rotate_target1.run(Classification.GARBAGE)
        time.sleep(2)
        rotate_target1.roll_back()
    elif test == '2':
        logger.debug(
            'Moving to bin: {}, {} degrees'.format(Classification.PAPER, BinLocation[Classification.PAPER]))
        rotate_target2 = RotateTarget(communication_manager.connection)
        rotate_target2.run(Classification.PAPER)
        time.sleep(2)
        rotate_target2.roll_back()
    elif test == '3':
        logger.debug(
            'Moving to bin: {} degrees, {} degrees'.format(Classification.GLASS, BinLocation[Classification.GLASS]))
        rotate_target3 = RotateTarget(communication_manager.connection)
        rotate_target3.run(Classification.GLASS)
        time.sleep(2)
        rotate_target3.roll_back()
    elif test == '4':
        logger.debug(
            'Moving to bin: {}, {} degrees'.format(Classification.RECYCLABLES,
                                                   BinLocation[Classification.RECYCLABLES]))
        rotate_target4 = RotateTarget(communication_manager.connection)
        rotate_target4.run(Classification.RECYCLABLES)
        time.sleep(2)
        rotate_target4.roll_back()

    logger.debug('closing the arduino connection')
    communication_manager.close_ard_connection()
