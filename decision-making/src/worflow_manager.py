from src.app_config import Waste, logging, Arduino, States, Pins, ConnectionManager, Classification
from src.steps.classify import Classify
from src.steps.drop import Drop
from src.tasks.arduino_manager import ArduinoManager
from src.tasks.bin_level import BinLevel
from src.tasks.camera_control import CameraControl
from src.tasks.communication_manager import CommunicationManager
from src.tasks.door_control import DoorControl
from src.tasks.item_detection import ItemDetection
from src.tasks.light_control import LightControl

logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self):
        pass

    # 1) detect if new item is ins1erted
    # 2) classify the item
    # 3) Drop the item
    def start(self):
        # part of the boot up, figuring out which arduino is which
        arduino_manager = ArduinoManager()
        arduino_manager.run()
        just_started = True
        while True:
            logger.debug('Stating all Arduinos connection')
            self.start_all_ard_connections()

            if just_started:
                self.change_system_state(States.CLOSE)
                just_started = False
                bin_level = BinLevel(ConnectionManager['mechanical'])
                bin_level.run()
                if bin_level.bin_full:
                    self.wait_until_bins_empty()
                    logger.debug('The bins are still full, the system is pausing')
                else:
                    logger.debug('the system is ready to run')
                    light_control = LightControl(ConnectionManager['mechanical'].connection,
                                                 Pins.BIN_LEVEL_LIGHT[0])
                    light_control.run(States.OPEN)

            logger.debug('Confirming that the door is closed and magnets are engaged')
            self.confirm_door_closed()

            # 1) Turn the System lights to green
            self.change_system_state(States.OPEN)

            logger.debug('Running Item Detection')
            # 2) start the item detection script
            item_detection = ItemDetection(ConnectionManager['detect_item'].ard_api,
                                           ConnectionManager['detect_item'].connection)
            item_detection.run()
            logger.debug('A new item has been inserted')
            # 3) If an new item is detected change the system lights to red
            self.change_system_state(States.CLOSE)
            # 4) then run thw classify and drop class
            waste = Waste()
            # classify_step = Classify(waste)
            # classify_step.run()
            camera_control = CameraControl(ConnectionManager['detect_item'])
            camera_control.take_picture_picam()
            waste.type = Classification.GLASS

            logger.debug('Classify step is done and the determined the waste type to be {}'.format(waste.type))
            drop_step = Drop(waste)
            drop_step.run()
            waste.status = drop_step.status
            logger.debug('Dropping step is done with status {} and waiting for a new item'.format(drop_step.status))
            # 5) if bins are full we need to hold the system until it is rebooted (basically infinite loop)
            if drop_step.system_hold:
                self.wait_until_bins_empty()
                logger.debug('The bin are full, the system is pausing')
            logger.debug('closing all the Arduinos connection')
            self.close_all_ard_connections()
            break

    def change_system_state(self, state):
        light_control = LightControl(ConnectionManager['mechanical'].connection, Pins.SYSTEM_LIGHT[0])
        light_control.run(state)

    def confirm_door_closed(self):
        door_control = DoorControl(ConnectionManager['detect_item'].connection)
        door_control.run(States.CLOSE)

    def wait_until_bins_empty(self):
        light_control = LightControl(ConnectionManager['mechanical'].connection, Pins.BIN_LEVEL_LIGHT[0])
        light_control.run(States.CLOSE)
        while True:
            pass

    def start_all_ard_connections(self):
        com_manager = CommunicationManager(Arduino['detect_item'])
        ConnectionManager['detect_item'] = com_manager
        com_manager = CommunicationManager(Arduino['mechanical'])
        ConnectionManager['mechanical'] = com_manager
        com_manager = CommunicationManager(Arduino['classification'])
        ConnectionManager['classification'] = com_manager

    def close_all_ard_connections(self):
        ConnectionManager['detect_item'].close_ard_connection()
        ConnectionManager['mechanical'].close_ard_connection()
        ConnectionManager['classification'].close_ard_connection()


if __name__ == '__main__':
    workflow_manager = WorkflowManager()
    logger.info('--------- Starting The Workflow Manager ----------')

    workflow_manager.start()
