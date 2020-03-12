from src.app_config import Classification
from src.tasks.camera_control import CameraControl
import os
import time
import logging
import numpy as np
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

logger = logging.getLogger(__name__)


class ComputerVision:
    def __init__(self):
        self.type = {}
        self.camera_control = CameraControl()
        self.image_location = None
        self.model_file = 'resources/new_mobile_model.tflite'
        self.labels = ['Garbage', 'Glass', 'Metal', 'Paper', 'Plastic']
        self.input_mean = 0
        self.input_std = 255

    def run(self):
        logger.debug('taking a picture and classifying it with computer vision')
        start_time = time.time()
        self.camera_control.take_picture()
        self.image_location = self.camera_control.image_location

        start_time2 = time.time()
        interpreter = tf.lite.Interpreter(model_path=self.model_file)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # check the type of the input tensor
        floating_model = input_details[0]['dtype'] == np.float32

        # NxHxWxC, H:1, W:2
        height = input_details[0]['shape'][1]
        width = input_details[0]['shape'][2]
        img = Image.open(self.image_location).resize((width, height))

        # add N dim
        input_data = np.expand_dims(img, axis=0)

        if floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std

        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        results = np.squeeze(output_data)

        top_k = results.argsort()[-5:][::-1]
        if floating_model:
            self.type[1] = Classification[self.labels[top_k[0]].upper()]
            self.type[2] = Classification[self.labels[top_k[1]].upper()] if self.within_ten_percent(
                float(results[top_k[0]]), float(results[top_k[1]])) else None
            logger.debug('Top type by computer vision is {}: {:08.6f}'.format(self.type[1], float(results[top_k[0]])))
        else:
            self.type[1] = Classification[self.labels[top_k[0]].upper()]
            self.type[2] = Classification[self.labels[top_k[1]].upper()] if self.within_ten_percent(
                float(results[top_k[0]] / 255), float(results[top_k[1]] / 255)) else None
            logger.debug('Top type by computer vision is {}: {:08.6f}'.format(self.type[1], float(results[top_k[0]])))

        end_time = time.time()
        elapsed_time1 = end_time - start_time
        elapsed_time2 = end_time - start_time2
        logger.debug('Elapsed time for CV with Camera: {} and without: {}'.format(elapsed_time1, elapsed_time2))

    def within_ten_percent(self, x, y):
        return True if (((x - y) / x) * 100) < 10 else False


if __name__ == '__main__':
    ComputerVision().run()
