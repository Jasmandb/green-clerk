import time
from collections import defaultdict
from src.app_config import Pins, logging, Constants
from nanpy import Ultrasonic

logger = logging.getLogger(__name__)


class BinLevel:
    def __init__(self, connection):
        self.connection = connection
        self.ultrasonics = []
        self.distance = defaultdict()
        self.first_meas = True
        self.bin_full = False
        self.bin_limit = Constants.BIN_ULTRASONIC_FULL_LEVEL

    def setup_ultrasonic_obj(self):
        for ping_pin, echo_pin in Pins.BIN_ULTRASONIC_PINS:
            self.ultrasonics.append((Ultrasonic(echo_pin, ping_pin, False, connection=self.connection), ping_pin))

    def run(self):
        logger.debug('Reading Information from the bin detection Ultrasonic sensors')
        self.setup_ultrasonic_obj()
        for ultrasonic, ping_pin in self.ultrasonics:
            self.distance[ping_pin] = ultrasonic.get_distance()
            time.sleep(0.001)

        for ultrasonic, ping_pin, in self.ultrasonics:
            if self.distance[ping_pin] - self.bin_limit < 0:
                self.bin_full = True
                logger.debug(
                    'Ultrasonic detection with ping_pin, reading: {}, {}'.format(ping_pin, self.distance[ping_pin]))


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager('/dev/ttyUSB0')

    logger.info('BinLevel')
    test = input('Enter a number: ')

    bin_level = BinLevel(communication_manager.connection)
    bin_level.run()
    logger.debug('Is bin_level full?: {}'.format(bin_level.bin_full))
    logger.debug('closing the arduino connection')

    communication_manager.close_ard_connection()
