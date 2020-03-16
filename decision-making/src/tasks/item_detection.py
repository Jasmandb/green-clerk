import time
from copy import deepcopy
from collections import defaultdict
from src.app_config import Pins
from nanpy import ArduinoApi, SerialManager, Ultrasonic
import logging

logger = logging.getLogger(__name__)


class ItemDetection:
    def __init__(self):
        self.connection = None
        self.ard_api = None
        self.ultrasonic = None
        self.distance = defaultdict()
        self.first_meas = True
        self.item_detected = False
        self.base_meas = None
        self.create_connection_channel()
        self.setup_pin_modes()

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            logger.debug('Starting a connection with the Arduino')
            self.connection = SerialManager(device='/dev/ttyACM1')
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logging.error('Failed to connect to Arduino {}'.format(str(e)))
            raise e

    def setup_pin_modes(self):
        for ping_pin, echo_pin in Pins.ULTRASONIC_PINS:
            self.ard_api.pinMode(ping_pin, self.ard_api.OUPUT)
            self.ard_api.pinMode(echo_pin, self.ard_api.INPUT)

        for ir_pin in Pins.IR_PINS:
            self.ard_api.pinMode(ir_pin, self.ard_api.INPUT)
            self.ard_api.digitalWrite(ir_pin, self.ard_api.HIGH)

    def run(self):
        logger.debug('Reading Information from the Ultrasonic sensors')
        while not self.item_detected:
            for ping_pin, echo_pin in Pins.ULTRASONIC_PINS:
                self.ultrasonic = Ultrasonic(echo_pin, ping_pin, False, connection=self.connection)
                self.distance[ping_pin] = self.ultrasonic.get_distance()
                time.sleep(0.001)

            if self.first_meas:
                self.first_meas = False
                self.base_meas = deepcopy(self.distance)

            for ping_pin, echo_pin in Pins.ULTRASONIC_PINS:
                if abs(self.base_meas[ping_pin] - self.first_meas[ping_pin]) > 2:
                    self.item_detected = True
                    logger.debug(
                        'Ultrasonic detection with ping_pin, echo_pin, reading: {}, {}, {}'.format(ping_pin, echo_pin,
                                                                                                   self.base_meas[
                                                                                                       ping_pin]))
            for ir_pin in Pins.IR_PINS:
                if self.ard_api.digitalRead(ir_pin) == self.ard_api.LOW:
                    self.item_detected = True
                    logger.debug('IR sensor detected an item')
            # TODO: Confirm with @Amneet: Why do we need to sleep for a second between each iteration?
            time.sleep(1)


if __name__ == '__main__':
    ItemDetection().run()
