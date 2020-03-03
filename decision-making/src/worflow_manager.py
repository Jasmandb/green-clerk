import logging

from src.tasks.camera_control import CameraControl

logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self):
        pass

    def start(self):
        pass


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
