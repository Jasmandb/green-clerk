from src.app_config import Step, States, logging, Pins, ConnectionManager
from src.tasks.bin_level import BinLevel
from src.tasks.door_control import DoorControl
from src.tasks.light_control import LightControl
from src.tasks.rotate_target import RotateTarget
import time

logger = logging.getLogger(__name__)


class Drop:
    def __init__(self, waste):
        self.door_control = DoorControl(ConnectionManager['detect_item'].connection)
        self.rotate_target = RotateTarget(ConnectionManager['detect_item'].connection)
        self.waste = waste
        self.waste.step = Step.DROP
        self.status = None
        self.bin_level = None
        self.light_control = None
        self.system_hold = False

    def run(self):
        logger.info('Running Drop step with waste type {}'.format(self.waste.type))
        self.rotate_target.run(bin_type=self.waste.type)
        logger.debug('Opening up door')
        self.door_control.run(States.OPEN)
        time.sleep(1)  # 2 second delay for item to drop. May need to modify this
        logger.debug('Closing door')
        self.door_control.run(States.CLOSE)
        self.rotate_target.roll_back()
        logger.debug('getting the bin levels')
        self.bin_level = BinLevel(ConnectionManager['mechanical'].connection)
        self.bin_level.run()
        if self.bin_level.bin_full:
            logger.debug('bin level is full')
            self.light_control = LightControl(ConnectionManager['mechanical'].connection, Pins.BIN_LEVEL_LIGHT[0])
            self.light_control.run(States.CLOSE)
            self.system_hold = True
        logger.debug('bin level exists with status: {}'.format(self.bin_level.bin_full))


if __name__ == '__main__':
    logger.info('dropping class')
    from src.app_config import Waste, Classification
    from src.tasks.arduino_manager import ArduinoManager
    from src.tasks.communication_manager import CommunicationManager
    from src.app_config import Arduino

    com_manager = CommunicationManager(Arduino['detect_item'])
    ConnectionManager['detect_item'] = com_manager
    com_manager = CommunicationManager(Arduino['mechanical'])
    ConnectionManager['mechanical'] = com_manager

    arduino_manager = ArduinoManager()
    arduino_manager.run()
    waste = Waste()
    waste.type = Classification.GLASS
    drop = Drop(waste)
    drop.run()
    logger.info('waste_type at classify class {}'.format(waste.type))
