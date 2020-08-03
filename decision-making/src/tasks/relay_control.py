from src.app_config import RelayStates, Pins, logging
from nanpy import Relay
from src.app_config import States, logging
from nanpy import Relay

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self, pin=None, connection):
        self.ard_api = None
        self.pin = None
        self.relay = None
        self.connection = connection

    def run(self, state):
        self.create_connection_channel()
        self.setup_relay_obj()
        logger.debug('The requested state is {}'.format(state))
        if state == States.OPEN:
            self.relay.open()
        else:
            self.relay.close()

    def setup_relay_obj(self):
        self.relay = Relay(self.pin, self.connection)


if __name__ == '__main__':
    from src.tasks.communication_manager import CommunicationManager

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager('/dev/ttyUSB0')
    logger.info('RelayControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            RelayControl().run(RelayStates.OPEN)
        else:
            RelayControl().run(RelayStates.CLOSE)
