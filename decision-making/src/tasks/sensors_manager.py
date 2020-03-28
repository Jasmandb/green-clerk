from src.app_config import Constants, Pins
from nanpy import ArduinoApi, SerialManager, Load
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class SensorsManager:
    def __init__(self):
        self.ard_api = None
        self.create_connection_channel()
        self.inductive = InductiveSensor(self.ard_api)
        self.capacitive = CapacitiveSensor(self.ard_api)
        self.weight = WeightSensor(self.ard_api)

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            self.ard_api = ArduinoApi(connection=SerialManager(device='/dev/ttyUSB0'))
        except Exception as e:
            logging.error('Failed to connect to Arduino {}'.format(str(e)))
            raise e

    def run(self):
        try:
            logger.debug('Storing the inductive sensors readings')
            self.inductive.store_sensor_readings()
            logger.debug('Storing the capacitive sensors readings')
            self.capacitive.store_sensor_readings()
            logger.debug('Storing the weight sensors readings')
            self.weight.store_sensor_readings()
        except Exception as e:
            logging.error('Unexpected Exception while reading the sensors: {}'.format(str(e)))
            raise e


class InductiveSensor:
    def __init__(self, ard_api):
        self.num_of_sensors_triggered = 0
        self.ard_api = ard_api
        self.inductive_pins = defaultdict(lambda: self.ard_api.HIGH)
        self.setup_pin_modes()
        # self.inductive_pins = {2: self.ard_api.HIGH, 3: self.ard_api.HIGH, 4: self.ard_api.HIGH, 5: self.ard_api.HIGH,
        #                        6: self.ard_api.HIGH, 7: self.ard_api.HIGH}

    def get_percentage_triggered(self):
        return (self.num_of_sensors_triggered / Constants.NUM_INDUCTIVE_SENSOR) * 100

    def store_sensor_readings(self):
        for pin in self.inductive_pins:
            temp = self.ard_api.digitalRead(pin)
            if temp != self.inductive_pins[pin]:
                if temp == self.ard_api.LOW:
                    self.num_of_sensors_triggered += 1
                self.inductive_pins[pin] = temp

    def setup_pin_modes(self):
        for pin in Pins.INDUCTIVE_PINS:
            self.ard_api.pinMode(pin, self.ard_api.INPUT)


class CapacitiveSensor:
    def __init__(self, ard_api):
        self.num_of_sensors_triggered = 0
        self.ard_api = ard_api
        self.capacitive_pins = defaultdict(lambda: self.ard_api.HIGH)
        self.setup_pin_modes()
        # self.capacitive_pins = {8: self.ard_api.HIGH, 9: self.ard_api.HIGH, 10: self.ard_api.HIGH,
        #                         11: self.ard_api.HIGH, 12: self.ard_api.HIGH, 13: self.ard_api.HIGH}

    def get_percentage_triggered(self):
        return (self.num_of_sensors_triggered / Constants.NUM_CAPACITIVE_SENSOR) * 100

    def store_sensor_readings(self):
        for pin in self.capacitive_pins:
            temp = self.ard_api.digitalRead(pin)
            if temp != self.capacitive_pins[pin]:
                if temp == self.ard_api.LOW:
                    self.num_of_sensors_triggered += 1
                self.capacitive_pins[pin] = temp

    def setup_pin_modes(self):
        for pin in Pins.CAPACITIVE_PINS:
            self.ard_api.pinMode(pin, self.ard_api.INPUT)


class WeightSensor:
    def __init__(self, ard_api):
        self.value = None
        self.ard_api = ard_api
        self.setup_weight_sensors_obj()
        self.weight_sensors = []

    def store_sensor_readings(self):
        for weight_sensor, data_out_pin in self.weight_sensors:
            self.value = weight_sensor.get_weight(20)
            logger.debug('weight sensor with data_out_pin {} read a value of {}'.format(data_out_pin, self.value))

    def setup_weight_sensors_obj(self):
        for data_out_pin, clock_pin, calibration_factor in Pins.WEIGHT_PINS:
            self.weight_sensors.append((Load(data_out_pin, clock_pin, calibration_factor), data_out_pin))


if __name__ == '__main__':
    logger.info('SensorsManager')
    SensorsManager().run()
