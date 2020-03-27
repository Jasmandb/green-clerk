import time
from src.app_config import Pins, BinLocation
from nanpy import ArduinoApi, SerialManager, Servo
import logging

logger = logging.getLogger(__name__)


class RotateTarget:
    def __init__(self):
        self.ard_api = None
        self.ard_id = '/dev/ttyACM0'
        self.servo = None
        self.bin_type = None
        self.step_size = 6
        self.create_connection_channel()
        self.setup_pin_modes()

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            self.ard_api = ArduinoApi(connection=SerialManager(device=self.ard_id))
        except Exception as e:
            logger.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def setup_pin_modes(self):
        # TODO: Since we are not expected to expand our number of motors this class is only coded for one motor
        # TODO: extend to have the ability to expand (I don't think this is necessary though)
        self.servo = Servo(Pins.SERVO_PINS[0])
        logger.debug('Servo pin {}'.format(Pins.SERVO_PINS[0]))

    def run(self, bin_type):
        self.bin_type = bin_type
        for angle in range(0, BinLocation[self.bin_type] + self.step_size, self.step_size):
            self.servo.writeMicroseconds(angle)
            time.sleep(0.01)

    def roll_back(self):
        for angle in range(BinLocation[self.bin_type], 0 - self.step_size, - self.step_size):
            self.servo.writeMicroseconds(angle)
            time.sleep(0.01)


if __name__ == '__main__':
    logger.info('RotateTarget')
    from src.app_config import Classification

    logger.debug('Moving to bin: {}, {} degrees'.format(Classification.GARBAGE, BinLocation[Classification.GARBAGE]))
    rotate_target1 = RotateTarget()
    rotate_target1.run(Classification.GARBAGE)
    rotate_target1.roll_back()
    time.sleep(1)

    logger.debug('Moving to bin: {}, {} degrees'.format(Classification.PAPER, BinLocation[Classification.PAPER]))
    rotate_target2 = RotateTarget()
    rotate_target2.run(Classification.PAPER)
    rotate_target2.roll_back()
    time.sleep(1)

    logger.debug(
        'Moving to bin: {} degrees, {} degrees'.format(Classification.GLASS, BinLocation[Classification.GLASS]))
    rotate_target3 = RotateTarget()
    rotate_target3.run(Classification.GLASS)
    rotate_target3.roll_back()
    time.sleep(1)

    logger.debug(
        'Moving to bin: {}, {} degrees'.format(Classification.RECYCLABLES, BinLocation[Classification.RECYCLABLES]))
    rotate_target4 = RotateTarget()
    rotate_target4.run(Classification.RECYCLABLES)
    rotate_target4.roll_back()
    time.sleep(1)
