from src.app_config import Waste, logging, Arduino, States, Pins, ConnectionManager
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
        self.start_all_ard_connections()
        self.confirm_door_closed()

        while True:
            logger.debug('Running Item Detection')
            self.change_system_status(States.OPEN)
            item_detection = ItemDetection(ConnectionManager['detect_item'].ard_api,
                                           ConnectionManager['detect_item'].connection)
            item_detection.run()
            logger.debug('A new item has been inserted')
            self.change_system_status(States.CLOSE)
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
        light_control = LightControl(ConnectionManager['mechanical'].connection, Pins.SYSTEM_LIGHT[0])
        light_control.run(state)

    def confirm_door_closed(self):
        door_control = DoorControl(ConnectionManager['detect_item'].connection)
        door_control.run(States.CLOSE)

    def wait_until_bins_empty(self):
        while True:
            pass

    def start_all_ard_connections(self):
        com_manager = CommunicationManager(Arduino['detect_item'])
        ConnectionManager['detect_item'] = com_manager
        com_manager = CommunicationManager(Arduino['mechanical'])
        ConnectionManager['mechanical'] = com_manager
        com_manager = CommunicationManager(Arduino['classification'])
        ConnectionManager['classification'] = com_manager


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
