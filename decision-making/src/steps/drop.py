from src.app_config import Step, States, logging, Arduino
from src.tasks.arduino_manager import ArduinoManager
from src.tasks.communication_manager import CommunicationManager
from src.tasks.door_control import DoorControl
from src.tasks.rotate_target import RotateTarget
import time

logger = logging.getLogger(__name__)


class Drop:
    def __init__(self, waste):
        self.com_manager = CommunicationManager(Arduino['detect_item'])
        self.door_control = DoorControl(self.com_manager.connection)
        self.rotate_target = RotateTarget(self.com_manager.connection)
        self.waste = waste
        self.waste.step = Step.DROP
        self.status = None

    def run(self):
        logger.info('Running Drop step with waste type {}'.format(self.waste.type))
        self.rotate_target.run(bin_type=self.waste.type)
        logger.debug('Opening up door')
        self.door_control.run(States.OPEN)
        time.sleep(2)  # 2 second delay for item to drop. May need to modify this
        logger.debug('Closing door')
        self.door_control.run(States.CLOSE)
        # TODO: Check if waste bin is full
        self.rotate_target.roll_back()


if __name__ == '__main__':
    logger.info('dropping class')
    from src.app_config import Waste, Classification
    arduino_manager = ArduinoManager()
    arduino_manager.run()
    waste = Waste()
    waste.type = Classification.GLASS
    drop = Drop(waste)
    drop.run()
    logger.info('waste_type at classify class {}'.format(waste.type))
