from src.app_config import Constants
from nanpy import ArduinoApi, SerialManager
import logging

logger = logging.getLogger(__name__)


class SensorsManager:
    def __init__(self):
        self.inductive = InductiveSensor()
        self.capacitive = CapacitiveSensor()
        self.weight = WeightSensor()
        self.ard_api = None
        self.create_connection_channel()
        self.inductive_pins = {2: self.ard_api.HIGH, 3: self.ard_api.HIGH, 4: self.ard_api.HIGH, 5: self.ard_api.HIGH,
                               6: self.ard_api.HIGH, 7: self.ard_api.HIGH}
        self.capacitive_pins = {8: self.ard_api.HIGH, 9: self.ard_api.HIGH, 1: self.ard_api.HIGH,
                                11: self.ard_api.HIGH, 12: self.ard_api.HIGH, 13: self.ard_api.HIGH}
        self.setup_pin_modes()

    def create_connection_channel(self):
        try:
            # TODO: change the device name to the actual device serial number after attaching a firmware to it
            self.ard_api = ArduinoApi(connection=SerialManager(device='/dev/ttyACM1'))
        except Exception as e:
            logging.error('Failed to connect to Arduino {}'.format(str(e)))
            raise e

    def setup_pin_modes(self):
        for pin in [*self.inductive_pins, *self.capacitive_pins]:
            self.ard_api.pinMode(pin, self.ard_api.INPUT)

    def run(self):
        try:
            for pin in self.inductive_pins:
                temp = self.ard_api.digitalRead(pin)
                if temp != self.inductive_pins[pin]:
                    if temp == self.ard_api.LOW:
                        self.inductive.num_of_sensors_triggered += 1
                    self.inductive_pins[pin] = temp

            for pin in self.capacitive_pins:
                temp = self.ard_api.digitalRead(pin)
                if temp != self.capacitive_pins[pin]:
                    if temp == self.ard_api.LOW:
                        self.capacitive.num_of_sensors_triggered += 1
                    self.capacitive_pins[pin] = temp
        except Exception as e:
            logging.error('Unexpected Exception while reading the sensors: {}'.format(str(e)))
            raise e


class InductiveSensor:
    def __init__(self):
        self.num_of_sensors_triggered = 0

    def get_percentage_triggered(self):
        return (self.num_of_sensors_triggered / Constants.NUM_INDUCTIVE_SENSOR) * 100


class CapacitiveSensor:
    def __init__(self):
        self.num_of_sensors_triggered = 0

    def get_percentage_triggered(self):
        return (self.num_of_sensors_triggered / Constants.NUM_CAPACITIVE_SENSOR) * 100


class WeightSensor:
    def __init__(self):
        self.value = None


if __name__ == '__main__':
    logger.info('SensorsManager')
    SensorsManager()
    # need for testing purposes
    # self.inductive_pins = {2: 'HIGH', 3: 'HIGH', 4: 'HIGH', 5: 'HIGH',
    #                        6: 'HIGH', 7: 'HIGH'}
    # self.capacitive_pins = {8: 'HIGH', 9: 'HIGH', 1: 'HIGH',
    #                         11: 'HIGH', 12: 'HIGH', 13: 'HIGH'}
