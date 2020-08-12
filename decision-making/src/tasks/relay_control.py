from src.app_config import States, logging
from nanpy import Relay

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self, connection, pin=None):
        self.pin = pin
        self.relay = None
        self.connection = connection

    def run(self, state):
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
    from src.app_config import Arduino

    logger.debug('starting new arduino connection')
    communication_manager = CommunicationManager(Arduino['detect_item'])
    logger.info('RelayControl')

    while True:
        test = input('Enter a number: ')
        if test == '1':
            RelayControl(communication_manager.connection, 5).run(States.OPEN)
        else:
            RelayControl(communication_manager.connection, 5).run(States.CLOSE)
