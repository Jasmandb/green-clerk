from enum import Enum, unique
import logging

logging.basicConfig(format='[%(asctime)s_%(levelname)s] %(name)s_%(module)s: %(message)s', level=logging.DEBUG)
logging.getLogger("pyserial").setLevel(logging.WARNING)


class Constants(int, Enum):
    INDUCTIVE_SENSOR_THRESHOLD = 17
    CAPACITIVE_SENSOR_THRESHOLD = 17
    WEIGHT = 136
    NUM_INDUCTIVE_SENSOR = 6
    NUM_CAPACITIVE_SENSOR = 6
    BIN_ULTRASONIC_FULL_LEVEL = 40


@unique
class Pins(list, Enum):
    INDUCTIVE_PINS = [2, 3, 4, 5, 6, 7]
    BIN_ULTRASONIC_PINS = []
    CAPACITIVE_PINS = [8, 9, 10, 11, 12, 13]
    ULTRASONIC_PINS = [(9, 8), (5, 4)]
    IR_PINS = [3]
    RELAY_PINS = [7]
    SERVO_PINS = [9]
    WEIGHT_PINS = [(14, 15, -1096.65)]


Arduino = {'item_detection': None, 'classification_sensors': None}


@unique
class ArduinoArsojaID(str, Enum):
    Arsoja_Arduino_2308_6030 = 'item_detection'


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
class RelayStates(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class Waste:
    def __init__(self):
        self.type = Classification.UNKNOWN
        self.status = Status.IN_PROGRESS
        self.step = None
        self.failure_messages = []
        self.workflow = {}
