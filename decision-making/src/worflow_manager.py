import logging
from src.tasks.sensors_manager import SensorsManager

logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self):
        sensors_manager = SensorsManager()
        # TODO: Currently this step running infinitely for POC in case for EP it would be triggered by the load step
        sensors_manager.run()

    def start(self):
        pass


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
