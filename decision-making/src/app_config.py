from enum import Enum, unique
import logging

# logging.basicConfig(filename='resources/app.log', filemode='w',
#                     format='[%(asctime)s_%(levelname)s] %(name)s_%(module)s: %(message)s', level=logging.DEBUG)
logging.basicConfig(format='[%(asctime)s_%(levelname)s] %(name)s_%(module)s: %(message)s', level=logging.DEBUG)
logging.getLogger("pyserial").setLevel(logging.WARNING)


class Constants(int, Enum):
    INDUCTIVE_SENSOR_THRESHOLD = 10
    CAPACITIVE_SENSOR_THRESHOLD = 10
    WEIGHT = 136
    NUM_INDUCTIVE_SENSOR = 6
    NUM_CAPACITIVE_SENSOR = 6
    BIN_ULTRASONIC_FULL_LEVEL = 30
    WEIGHT_SENSOR_OFFSET = -18727
    DETECTION_ULTRASONIC_DIFF = 2


@unique
class Pins(list, Enum):
    INDUCTIVE_PINS = [4, 5, 8, 9, 12, 13]
    CAPACITIVE_PINS = [2, 3, 6, 7, 10, 11]
    ULTRASONIC_PINS = [(8, 7), (6, 5)]
    IR_PINS = [9]
    FLASH_PIN = [14]
    SERVO_PINS = [3]
    WEIGHT_PINS = [(15, 14, -262.0)]
    DOOR = [11, 12, 10]
    BIN_ULTRASONIC_PINS = [(6, 7), (8, 9), (10, 11), (12, 13)]
    BIN_LEVEL_LIGHT = [(2, 3)]
    SYSTEM_LIGHT = [(4, 5)]


Arduino = {'detect_item': None, 'classification': None, 'mechanical': None}
ConnectionManager = {'detect_item': None, 'classification': None, 'mechanical': None}


@unique
class ArduinoArsojaID(str, Enum):
    Arsoja_Arduino_3616_2060 = 'detect_item'
    Arsoja_Arduino_3501_4781 = 'classification'
    Arsoja_Arduino_6956_1790 = 'mechanical'


@unique
class Classification(str, Enum):
    GARBAGE = 'GARBAGE'
    PAPER = 'PAPER'
    GLASS = 'GLASS'
    METAL = 'METAL'
    RECYCLABLES = 'RECYCLABLES'
    UNKNOWN = 'UNKNOWN'
    PLASTIC = 'PLASTIC'


@unique
class BinLocation(int, Enum):
    GARBAGE = 0
    PAPER = 90
    GLASS = 180
    RECYCLABLES = 270


@unique
class BinLevel(str, Enum):
    FULL = 'FULL'
    THRESHOLD = 'THRESHOLD'
    EMPTY = 'EMPTY'


@unique
class SensingStation(str, Enum):
    LOADING = 'LOADING'
    DROPPING = 'DROPPING'
    CLASSIFYING = 'CLASSIFYING'
    STUCK = 'STUCK'


@unique
class Status(str, Enum):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    IN_PROGRESS = 'IN_PROGRESS'


@unique
class Step(str, Enum):
    LOAD = 'LOAD'
    CLASSIFY = 'CLASSIFY'
    DROP = 'DROP'


@unique
class States(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class Waste:
    def __init__(self):
        self.type = Classification.UNKNOWN
        self.status = Status.IN_PROGRESS
        self.step = None
        self.failure_messages = []
        self.workflow = {}
