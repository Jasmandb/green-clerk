from src.app_config import Waste, logging, Arduino, States, Pins
from src.steps.classify import Classify
from src.steps.drop import Drop
from src.tasks.arduino_manager import ArduinoManager
from src.tasks.communication_manager import CommunicationManager
from src.tasks.door_control import DoorControl
from src.tasks.item_detection import ItemDetection
from src.tasks.light_control import LightControl

logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self):
        pass

    # 1) detect if new item is ins1erted
    # 2) classify the item
    # 3) Drop the item
    def start(self):
        arduino_manager = ArduinoManager()
        arduino_manager.run()
        self.confirm_door_closed()

        while True:
            logger.debug('Running Item Detection')
            self.change_system_status(States.OPEN)
            com_manager = CommunicationManager(Arduino['detect_item'])
            item_detection = ItemDetection(com_manager.ard_api, com_manager.connection)
            item_detection.run()
            com_manager.close_ard_connection()
            self.change_system_status(States.CLOSE)
            logger.debug('A new item has been inserted')
            waste = Waste()
            classify_step = Classify(waste)
            classify_step.run()
            logger.debug('Classify step is done and the determined the waste type to be {}'.format(waste.type))
            drop_step = Drop(waste)
            drop_step.run()
            waste.status = drop_step.status
            if drop_step.system_hold:
                self.wait_until_bins_empty()
            logger.debug('Dropping step is done with status {} and waiting for a new item'.format(drop_step.status))

    def change_system_status(self, state):
        com_manager = CommunicationManager(Arduino['mechanical'])
        light_control = LightControl(com_manager.connection, Pins.SYSTEM_LIGHT[0])
        light_control.run(state)
        com_manager.close_ard_connection()

    def confirm_door_closed(self):
        com_manager = CommunicationManager(Arduino['detect_item'])
        door_control = DoorControl(com_manager.connection)
        door_control.run(States.CLOSE)
        com_manager.close_ard_connection()

    def wait_until_bins_empty(self):
        pass


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
