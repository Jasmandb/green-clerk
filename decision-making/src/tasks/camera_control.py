import src.app_config
import logging

logger = logging.getLogger(__name__)


class CameraControl:
    def __init__(self):
        self.image_location = None

    def take_picture(self):
        pass


if __name__ == '__main__':
    logger.info('hello world')
