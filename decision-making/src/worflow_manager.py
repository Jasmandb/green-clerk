from src.app_config import Waste, logging, Arduino
from src.steps.classify import Classify
from src.steps.drop import Drop
from src.tasks.arduino_manager import ArduinoManager
from src.tasks.communication_manager import CommunicationManager
from src.tasks.item_detection import ItemDetection

logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self):
        pass

    # 1) detect if new item is inserted
    # 2) classify the item
    # 3) Drop the item
    def start(self):
        arduino_manager = ArduinoManager()
        arduino_manager.run()
        while True:
            logger.debug('Running Item Detection')
            com_manager = CommunicationManager(Arduino['detect_item'])
            item_detection = ItemDetection(com_manager.ard_api, com_manager.connection)
            item_detection.run()
            com_manager.close_ard_connection()
            logger.debug('A new item has been inserted')
            waste = Waste()
            classify_step = Classify(waste)
            classify_step.run()
            logger.debug('Classify step is done and the determined the waste type to be {}'.format(waste.type))
            drop_step = Drop(waste)
            drop_step.run()
            waste.status = drop_step.status
            logger.debug('Dropping step is done with status {} and waiting for a new item'.format(drop_step.status))


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
