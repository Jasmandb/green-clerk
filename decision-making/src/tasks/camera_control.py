import logging
import cv2

logger = logging.getLogger(__name__)


class CameraControl:
    def __init__(self):
        self.image_location = '../../resources/webcam_img.jpg'
        self.image_width = 1280
        self.image_height = 720

    def take_picture(self):
        cam = cv2.VideoCapture(0)
        if cam.isOpened():
            logger.debug('webcam connection opened')
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)

            logger.debug('taking a picture with webcam')
            ret, img = cam.read()  # ret is true upon success
            logger.debug('saving picture for access by computer vision')
            cv2.imwrite(self.image_location, img)

            cam.release()
            logger.debug('webcam connection closed')
        else:
            # TODO: what do we do if camera not found?
            logger.error('webcam could not be accessed')


if __name__ == '__main__':
    logger.info('Starting CameraControl and taking a picture')
    CameraControl().take_picture()
