from src.app_config import Step, RelayStates, logging
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
        self.status = None

    def run(self):
        logger.info('Running Drop step with waste type {}'.format(self.waste.type))
        self.rotate_target.run(bin_type=self.waste.type)
        logger.debug('Opening up relay')
        self.relay_control.run(RelayStates.OPEN)
        input('Please enter anything when door is closed: ')
        # TODO: Maybe wait a little to confirm item dropped (add IR sensor input here maybe)
        self.relay_control.run(RelayStates.CLOSE)
        self.relay_control.close_ard_connection()
        self.rotate_target.roll_back()


if __name__ == '__main__':
    logger.info('dropping class')
    from src.app_config import Waste, Classification
    waste = Waste()
    waste.type = Classification.GLASS
    drop = Drop(waste)
    drop.run()
    logger.info('waste_type at classify class {}'.format(waste.type))
