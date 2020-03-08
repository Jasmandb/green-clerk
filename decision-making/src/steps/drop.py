from src.app_config import Step, BinLocation, BinLevel, RelayStates
import logging
from src.tasks.relay_control import RelayControl
from src.tasks.rotate_target import RotateTarget

logger = logging.getLogger(__name__)

# TODO: COMPLETE THE DROP CLASS

'''
Need the following steps:
 - Rotate to Target position applicable
 - Open the door to drop the item
 - Close the door 
 - Rotate to home position if applicable
'''


class Drop:
    def __init__(self, waste):
        self.rotate_target = RotateTarget()
        self.relay_control = RelayControl()
        self.waste = waste
        self.waste.step = Step.DROP

    def run(self):
        self.rotate_target.run(bin_type=BinLocation[self.waste.type])
        self.relay_control.run(RelayStates.OPEN)
        # TODO: Maybe wait a little to confirm item dropped (add IR sensor input here maybe)
        self.relay_control.run(RelayStates.CLOSE)
        self.rotate_target.run(bin_type=BinLocation.DEFAULT)


if __name__ == '__main__':
    logger.info('hello world')
