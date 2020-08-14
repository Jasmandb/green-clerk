from src.app_config import logging, Pins, States, ConnectionManager
import cv2
from time import sleep
from picamera import PiCamera

from src.tasks.relay_control import RelayControl

logger = logging.getLogger(__name__)


class CameraControl:
    def __init__(self, connection):
        self.image_location = 'resources/webcam_img.jpg'
        self.image_width = 1280
        self.image_height = 720
        self.connection = connection

    def take_picture(self):
        try:
            cam = cv2.VideoCapture(0)
            logger.debug('webcam connection opened')
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)

            logger.debug('taking a picture with webcam')
            ret, img = cam.read()  # ret is true upon success
            logger.debug('saving picture for access by computer vision')
            cv2.imwrite(self.image_location, img)

            cam.release()
            logger.debug('webcam connection closed')
        except Exception as e:
            logger.error('Failed to access the webcam with exception {}'.format(str(e)))
            raise e

    def take_picture_picam(self):
        try:
            relay_control = RelayControl(self.connection, Pins.FLASH_PIN[0])
            relay_control.run(States.OPEN)
            camera = ConnectionManager['camera']
            camera.resolution = (1024, 768)
            camera.start_preview()
            sleep(2)  # Camera warm-up time
            camera.capture(self.image_location, resize=(320, 240))
            camera.stop_preview()
            relay_control.run(States.CLOSE)
        except Exception as e:
            logger.error('Failed to access the webcam with exception {}'.format(e))
            raise e


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager
    from src.app_config import Arduino
    logger.info('Starting CameraControl and taking a picture')

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager(Arduino['detect_item'])
    logger.info('CameraControl')

    CameraControl(communication_manager.connection).take_picture()

    communication_manager.close_ard_connection()
