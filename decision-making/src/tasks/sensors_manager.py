import src.app_config
import logging

logger = logging.getLogger(__name__)


class SensorsManager:
    def __init__(self):
        self.inductive = InductiveSensor()
        self.capacitive = CapacitiveSensor()
        self.weight = WeightSensor()

    def run(self):
        pass


class InductiveSensor:
    def __init__(self):
        self.percentage_triggered = None


class CapacitiveSensor:
    def __init__(self):
        self.percentage_triggered = None


class WeightSensor:
    def __init__(self):
        self.value = None


if __name__ == '__main__':
    logger.info('hello world')
