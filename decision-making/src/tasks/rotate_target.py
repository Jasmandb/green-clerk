import src.app_config
import logging

logger = logging.getLogger(__name__)


class RotateTarget:
    def __init__(self):
        pass

    def run(self, bin_type):
        # TODO: add functionality for controlling stepper motor
        self.stepper_motor_control(bin_type)

    def stepper_motor_control(self, bin_type):
        # TODO: Rotate to degrees = bin_type.value
        pass


if __name__ == '__main__':
    logger.info('hello world')
