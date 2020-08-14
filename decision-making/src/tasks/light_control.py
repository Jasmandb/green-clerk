from src.app_config import States, logging
from nanpy import Light

logger = logging.getLogger(__name__)


class LightControl:
    def __init__(self, connection, pin=None):
        self.red_pin = pin[0]
        self.green_pin = pin[1]
        self.light = None
        self.connection = connection

    def run(self, state):
        self.setup_light_obj()
        logger.debug('The requested state is {}'.format(state))
        if state == States.OPEN:
            self.light.start()
        else:
            self.light.stop()

    def setup_light_obj(self):
        self.light = Light(self.red_pin, self.green_pin, self.connection)


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager
    from src.tasks.arduino_manager import ArduinoManager
    from src.app_config import Arduino, Pins

    logger.debug('starting new arduino connection')

    arduino_manager = ArduinoManager()
    communication_manager = CommunicationManager(Arduino['mechanical'])
    logger.info('LightControl')

    test = input('Enter a number: ')
    if test == '1':
        LightControl(communication_manager.connection, Pins.SYSTEM_LIGHT[0]).run(States.OPEN)
    else:
        LightControl(communication_manager.connection, Pins.SYSTEM_LIGHT[0]).run(States.CLOSE)

    communication_manager.close_ard_connection()
