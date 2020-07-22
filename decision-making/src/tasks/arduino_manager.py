from src.app_config import Arduino, logging, ArduinoArsojaID
from nanpy import ArduinoApi, SerialManager, EEPROMCont
from serial.tools import list_ports

logger = logging.getLogger(__name__)


class ArduinoManager:

    def __init__(self):
        self.ard_api = None
        self.ard_id = None
        self.connection = None
        self.eeprom = None
        self.ard_devices = set()

    def run(self):
        self.get_ard_devices()
        for ard_device in self.ard_devices:
            self.ard_id = ard_device
            self.create_connection_channel()
            self.setup_EEPROM_obj()
            arsoja_id = self.eeprom.get_id()
            arsoja_id = arsoja_id.replace('-', '_')
            try:
                Arduino[ArduinoArsojaID[arsoja_id]] = self.ard_id
            except Exception as e:
                logger.error('Failed to find the arsoja_id: {} in known Arduinos with error {}'.format(arsoja_id, e))
                raise e
            self.close_ard_connection()

    def get_ard_devices(self):
        usb_devices = list_ports.comports()
        for usb_device in usb_devices:
            if 'USB' in usb_device.name or 'ACM' in usb_device.name:
                self.ard_devices.add(usb_device.device)

    def setup_EEPROM_obj(self):
        self.eeprom = EEPROMCont(self.connection)

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
    # test: print all the ard devices
    ard_manager = ArduinoManager()
    ard_manager.run()
    print('Test item detection {}'.format(Arduino['item_detection']))
