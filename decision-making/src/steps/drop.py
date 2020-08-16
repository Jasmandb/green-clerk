from src.app_config import Step, States, logging, ConnectionManager, Arduino
from src.tasks.bin_level import BinLevel
from src.tasks.door_control import DoorControl
from src.tasks.rotate_target import RotateTarget
from src.tasks.communication_manager import CommunicationManager
import time

logger = logging.getLogger(__name__)


class Drop:
    def __init__(self, waste):
        self.rotate_target = None
        self.door_control = None
        self.waste = waste
        self.waste.step = Step.DROP
        self.status = None
        self.bin_level = None
        self.light_control = None
        self.system_hold = False

    def run(self):
        logger.info('Running Drop step with waste type {}'.format(self.waste.type))
        self.rotate_target = RotateTarget(ConnectionManager['detect_item'].connection)
        self.rotate_target.run(bin_type=self.waste.type)
        ConnectionManager['detect_item'].close_ard_connection()
        ConnectionManager['detect_item'] = CommunicationManager(Arduino['detect_item'])
        logger.debug('Opening up door')
        self.door_control = DoorControl(ConnectionManager['detect_item'].connection)
        self.door_control.run(States.OPEN)
        time.sleep(1)  # 2 second delay for item to drop. May need to modify this
        logger.debug('Closing door')
        self.door_control.run(States.CLOSE)
        ConnectionManager['detect_item'].close_ard_connection()
        ConnectionManager['detect_item'] = CommunicationManager(Arduino['detect_item'])
        self.rotate_target = RotateTarget(ConnectionManager['detect_item'].connection)
        self.rotate_target.roll_back(bin_type=self.waste.type)
        logger.debug('getting the bin levels')
        self.bin_level = BinLevel(ConnectionManager['mechanical'].connection)
        self.bin_level.run()
        if self.bin_level.bin_full:
            logger.debug('bin level is full')
            self.system_hold = True
        logger.debug('bin level exists with status: {}'.format(self.bin_level.bin_full))


if __name__ == '__main__':
    logger.info('dropping class')
    from src.app_config import Waste, Classification
    from src.tasks.arduino_manager import ArduinoManager
    # from src.tasks.communication_manager import CommunicationManager
    # from src.app_config import Arduino

    arduino_manager = ArduinoManager()
    arduino_manager.run()
    com_manager = CommunicationManager(Arduino['detect_item'])
    ConnectionManager['detect_item'] = com_manager
    com_manager = CommunicationManager(Arduino['mechanical'])
    ConnectionManager['mechanical'] = com_manager

    waste = Waste()
    waste.type = Classification.GLASS
    drop = Drop(waste)
    drop.run()
    logger.info('waste_type at classify class {}'.format(waste.type))
