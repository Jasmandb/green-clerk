import logging
from src.app_config import Waste
from src.steps.classify import Classify
from src.steps.drop import Drop
from src.tasks.item_detection import ItemDetection


logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self):
        self.item_detection = ItemDetection()
        self.waste = None

    def start(self):
        while True:
            logger.debug('Running Item Detection')
            self.item_detection.run()
            logger.debug('A new item has been inserted')
            self.waste = Waste()
            classify_step = Classify(self.waste)
            classify_step.run()
            logger.debug('Classify step is done and the determined the waste type to be {}'.format(self.waste.type))
            drop_step = Drop(self.waste)
            self.waste.status = drop_step.status
            logger.debug('Dropping step is done with status {} and waiting for a new item'.format(drop_step.status))


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
