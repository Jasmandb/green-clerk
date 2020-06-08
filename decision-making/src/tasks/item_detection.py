import time
from copy import deepcopy
from collections import defaultdict
from src.app_config import Pins, Arduino, logging
from nanpy import ArduinoApi, SerialManager, Ultrasonic

logger = logging.getLogger(__name__)


class ItemDetection:
    def __init__(self):
        self.connection = None
        self.ard_api = None
        self.ard_id = Arduino.ard_3
        self.ultrasonics = []
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
            self.connection = SerialManager(device=self.ard_id)
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logger.error('Failed to connect to Arduino {}'.format(str(e)))
            raise e

    def setup_pin_modes(self):
        for ping_pin, echo_pin in Pins.ULTRASONIC_PINS:
            self.ard_api.pinMode(ping_pin, self.ard_api.OUTPUT)
            self.ard_api.pinMode(echo_pin, self.ard_api.INPUT)

        for ir_pin in Pins.IR_PINS:
            self.ard_api.pinMode(ir_pin, self.ard_api.INPUT)
            self.ard_api.digitalWrite(ir_pin, self.ard_api.HIGH)

    def setup_ultrasonic_obj(self):
        for ping_pin, echo_pin in Pins.ULTRASONIC_PINS:
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
        self.close_ard_connection()

    def close_ard_connection(self):
        self.connection.close()


if __name__ == '__main__':
    ItemDetection().run()
