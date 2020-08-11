import time
from copy import deepcopy
from collections import defaultdict
from src.app_config import Pins, logging
from nanpy import Ultrasonic

logger = logging.getLogger(__name__)


class ItemDetection:
    def __init__(self, ard_api, connection):
        self.ard_api = ard_api
        self.connection = connection
        self.ultrasonics = []
        self.distance = defaultdict()
        self.first_meas = True
        self.item_detected = False
        self.base_meas = None
        self.setup_pin_modes()

    def setup_pin_modes(self):
        for ir_pin in Pins.IR_PINS:
            self.ard_api.pinMode(ir_pin, self.ard_api.INPUT)
            self.ard_api.digitalWrite(ir_pin, self.ard_api.HIGH)

    def setup_ultrasonic_obj(self):
        for echo_pin, ping_pin in Pins.ULTRASONIC_PINS:
            self.ultrasonics.append((Ultrasonic(echo_pin, ping_pin, False, connection=self.connection), ping_pin))

    def run(self):
        logger.debug('Reading Information from the Ultrasonic sensors')
        self.setup_ultrasonic_obj()
        while not self.item_detected:
            for ultrasonic, ping_pin in self.ultrasonics:
                self.distance[ping_pin] = ultrasonic.get_distance()
                time.sleep(0.001)

            if self.first_meas:
                self.first_meas = False
                self.base_meas = deepcopy(self.distance)

            for ultrasonic, ping_pin, in self.ultrasonics:
                if abs(self.base_meas[ping_pin] - self.distance[ping_pin]) > 2:
                    self.item_detected = True
                    logger.debug(
                        'Ultrasonic detection with ping_pin, reading: {}, {}'.format(ping_pin, self.distance[ping_pin]))
            for ir_pin in Pins.IR_PINS:
                if self.ard_api.digitalRead(ir_pin) == self.ard_api.LOW:
                    self.item_detected = True
                    logger.debug('IR sensor detected an item')


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager('/dev/ttyUSB0')
    ItemDetection(communication_manager.ard_api, communication_manager.connection).run()
    logger.debug('closing the arduino connection')
    communication_manager.close_ard_connection()
