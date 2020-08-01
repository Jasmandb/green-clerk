from src.app_config import RelayStates, Pins, logging
from nanpy import Relay

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self, connection):
        self.relay = None
        self.connection = connection

    def run(self, state):
        self.setup_relay_obj()
        if state == RelayStates.OPEN:
            logger.debug('Opening the lid requested state is {}'.format(state))
            # self.ard_api.digitalWrite(Pins.RELAY_PINS[0], self.ard_api.LOW)
            self.relay.open()
        else:
            logger.debug('Closing the lid requested state is state {}'.format(state))
            # self.ard_api.digitalWrite(Pins.RELAY_PINS[0], self.ard_api.HIGH)
            self.relay.close()

    def setup_relay_obj(self):
        # TODO: Since we are not expected to expand our number of relays this class is only coded for one sensor
        # TODO: extend to have the ability to expand (I don't think this is necessary though)
        # self.ard_api.pinMode(Pins.RELAY_PINS[0], self.ard_api.OUTPUT)
        self.relay = Relay(Pins.RELAY_PINS[0], self.connection)


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager('/dev/ttyUSB0')
    logger.info('RelayControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            RelayControl(communication_manager.connection).run(RelayStates.OPEN)
        else:
            RelayControl(communication_manager.connection).run(RelayStates.CLOSE)

    communication_manager.close_ard_connection()
