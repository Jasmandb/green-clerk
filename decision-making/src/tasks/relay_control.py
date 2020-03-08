from src.app_config import RelayStates
import logging

logger = logging.getLogger(__name__)


class RelayControl:
    def __init__(self):
        pass

    def run(self, state):
        self.set_relay_state(state)

    def set_relay_state(self, state):
        if state == RelayStates.OPEN:
            pass
        elif state == RelayStates.CLOSE:
            pass


if __name__ == '__main__':
    logger.info('hello world')
