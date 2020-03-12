from src.app_config import Step, Classification, Constants
import logging
from src.tasks.sensors_manager import SensorsManager
from src.tasks.computer_vision import ComputerVision

logger = logging.getLogger(__name__)


class Classify:
    def __init__(self, waste):
        self.sensors_manager = SensorsManager()
        self.computer_vision = ComputerVision()
        self.waste = waste
        self.waste.step = Step.CLASSIFY
        self.waste.workflow[Step.CLASSIFY] = {}  # TODO: Can be changed to string later depending on the steps classes

    def run(self):
        logger.info('Running the classifying class')
        self.computer_vision.run()
        self.sensors_manager.run()
        if self.sensors_manager.inductive.get_percentage_triggered() > Constants.INDUCTIVE_SENSOR_THRESHOLD:
            self.waste.type = Classification.METAL
            return

        if self.sensors_manager.inductive.get_percentage_triggered() != 0:
            self.inductive_sensor_below_threshold()
        elif self.sensors_manager.capacitive.get_percentage_triggered() > Constants.CAPACITIVE_SENSOR_THRESHOLD:
            self.capacitive_sensor_above_threshold()
        elif self.sensors_manager.capacitive.get_percentage_triggered() != 0:
            self.capacitive_sensor_below_threshold()
        else:
            self.no_sensor_triggered()

    def inductive_sensor_below_threshold(self):
        logger.debug('The inductive sensor is below the threshold.')
        if self.computer_vision.type[1] == Classification.GLASS:
            self.waste.type = Classification.GLASS
        else:
            self.waste.type = Classification.RECYCLABLES

    def capacitive_sensor_below_threshold(self):
        logger.debug('The capacitive sensor is below the threshold.')
        heavy_item = self.sensors_manager.weight.value > Constants.WEIGHT
        if self.computer_vision.type[1] == Classification.PAPER and not heavy_item:
            self.waste.type = Classification.PAPER
        elif self.computer_vision.type[1] == Classification.GLASS:
            self.waste.type = Classification.GLASS
        elif self.computer_vision.type[1] == Classification.PLASTIC and not heavy_item:
            self.waste.type = Classification.GLASS
        else:
            self.waste.type = Classification.GARBAGE

    def capacitive_sensor_above_threshold(self):
        logger.debug('The capacitive sensor is above the threshold.')
        heavy_item = self.sensors_manager.weight.value > Constants.WEIGHT
        if self.computer_vision.type[1] == Classification.PAPER and not heavy_item:
            self.waste.type = Classification.PAPER
        elif self.computer_vision.type[1] == Classification.GLASS:
            self.waste.type = Classification.GLASS
        elif self.computer_vision.type[1] == Classification.PLASTIC and heavy_item and self.computer_vision.type[
            2] and self.computer_vision.type[2] == Classification.GLASS:
            self.waste.type = Classification.GLASS
        elif self.computer_vision.type[1] == Classification.PLASTIC and not heavy_item and self.computer_vision.type[
            2] and self.computer_vision.type[2] != Classification.GARBAGE:
            self.waste.type = Classification.RECYCLABLES
        else:
            self.waste.type = Classification.GARBAGE

    def no_sensor_triggered(self):
        logger.debug('No sensor was triggered')
        heavy_item = self.sensors_manager.weight.value > Constants.WEIGHT
        if not heavy_item and self.computer_vision.type[1] == Classification.PAPER:
            self.waste.type = Classification.PAPER
        elif not heavy_item and self.computer_vision.type[1] == Classification.PLASTIC:
            self.waste.type = Classification.PLASTIC
        else:
            self.waste.type = Classification.GARBAGE


if __name__ == '__main__':
    logger.info('hello world')
