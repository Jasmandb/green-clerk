from src.app_config import Arduino, logging
from nanpy import ArduinoApi, SerialManager
from serial.tools import list_ports

logger = logging.getLogger(__name__)


class ArduinoManager:

    def __init__(self):
        self.EEPROM_SIZE = 1024
        self.ard_api = None
        self.ard_id = None
        self.connection = None
        self.eeprom = None
        self.ard_devices = set()

    def run(self):
        for ard_device in self.ard_devices:
            # 1) need to get the id from the firmware
            # 2) assign the id to the right name
            # 3) do the following for each device
            # 4) Do not forget to close the connection
            self.create_connection_channel()
            self.setup_relay_obj()
            pass

    def enumerate_serial_devices(self):
        usb_devices = list_ports.comports()
        for usb_device in usb_devices:
            if 'USB' in usb_device.name or 'ACM' in usb_device.name:
                self.ard_devices.add(usb_device.device)

    def setup_relay_obj(self):
        self.eeprom = None

    def create_connection_channel(self):
        try:
            self.connection = SerialManager(device=self.ard_id)
            self.ard_api = ArduinoApi(connection=self.connection)
        except Exception as e:
            logging.error('Failed to connect to ard_id: {} and error: {}'.format(self.ard_id, str(e)))
            raise e

    def close_ard_connection(self):
        self.connection.close()


if __name__ == '__main__':
    # test 1: print all the ard devices
    ard_manager = ArduinoManager()
    ard_manager.enumerate_serial_devices()
    print('Ard devices found {}'.format(ard_manager.ard_devices))
