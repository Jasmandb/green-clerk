from src.app_config import Constants, Pins, logging
from nanpy import Load
from collections import defaultdict

logger = logging.getLogger(__name__)


class SensorsManager:
    def __init__(self, ard_api, connection):
        self.ard_api = ard_api
        self.connection = connection
        self.inductive = InductiveSensor(self.ard_api)
        self.capacitive = CapacitiveSensor(self.ard_api)
        self.weight = WeightSensor(self.ard_api, self.connection)

    def run(self):
        try:
            logger.debug('Storing the inductive sensors readings')
            self.inductive.store_sensor_readings()
            logger.debug('Storing the capacitive sensors readings')
            self.capacitive.store_sensor_readings()
            logger.debug('Storing the weight sensors readings')
            self.weight.store_sensor_readings()
        except Exception as e:
            logger.error('Unexpected Exception while reading the sensors: {}'.format(str(e)))
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
        for pin in Pins.INDUCTIVE_PINS:
            temp = self.ard_api.digitalRead(pin)
            # logger.debug('inductive_pins[pin]: {}'.format(self.inductive_pins[pin]))
            if temp != self.inductive_pins[pin]:
                if temp == self.ard_api.LOW:
                    self.num_of_sensors_triggered += 1
                self.inductive_pins[pin] = temp
        logger.info('Number of inductive sensor triggered {}'.format(self.num_of_sensors_triggered))

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
        for pin in Pins.CAPACITIVE_PINS:
            temp = self.ard_api.digitalRead(pin)
            if temp != self.capacitive_pins[pin]:
                if temp == self.ard_api.LOW:
                    self.num_of_sensors_triggered += 1
                self.capacitive_pins[pin] = temp
        logger.info('Number of capacitive sensor triggered {}'.format(self.num_of_sensors_triggered))

    def setup_pin_modes(self):
        for pin in Pins.CAPACITIVE_PINS:
            self.ard_api.pinMode(pin, self.ard_api.INPUT)


class WeightSensor:
    def __init__(self, ard_api, connection):
        self.value = None
        self.conversion_factor = 1000
        self.offset = -18526
        self.ard_api = ard_api
        self.connection = connection
        self.weight_sensors = []
        self.setup_weight_sensors_obj()

    def store_sensor_readings(self):
        for weight_sensor, data_out_pin in self.weight_sensors:
            self.value = (weight_sensor.get_weight(20) * self.conversion_factor) + self.offset
            logger.debug('weight sensor with data_out_pin {} read a value of {}'.format(data_out_pin, self.value))

    def setup_weight_sensors_obj(self):
        for data_out_pin, clock_pin, calibration_factor in Pins.WEIGHT_PINS:
            self.weight_sensors.append(
                (Load(data_out_pin, clock_pin, calibration_factor, self.connection), data_out_pin))


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager('/dev/ttyUSB0')
    logger.info('SensorsManager')
    sensor_manager = SensorsManager(communication_manager.ard_api, communication_manager.connection)
    sensor_manager.run()
    logger.debug('num_of_ind_sensors_triggered: {}, num_of_cap_sensors_triggered: {} weight_value: {}'.format(
        sensor_manager.inductive.num_of_sensors_triggered, sensor_manager.capacitive.num_of_sensors_triggered,
        sensor_manager.weight.value))
    logger.debug('closing the arduino connection')
    communication_manager.close_ard_connection()
