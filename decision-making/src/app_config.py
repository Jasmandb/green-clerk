from enum import Enum, unique
import logging

logging.basicConfig(format='[%(asctime)s_%(levelname)s] %(name)s_%(module)s: %(message)s', level=logging.DEBUG)
logging.getLogger('nanpy').addHandler(logging.NullHandler())


class Constants(int, Enum):
    INDUCTIVE_SENSOR_THRESHOLD = 1
    CAPACITIVE_SENSOR_THRESHOLD = 1
    WEIGHT = 100
    NUM_INDUCTIVE_SENSOR = 6
    NUM_CAPACITIVE_SENSOR = 6


@unique
class Pins(list, Enum):
    INDUCTIVE_PINS = [2, 3, 4, 5, 6, 7]
    CAPACITIVE_PINS = [8, 9, 10, 11, 12, 13]
    ULTRASONIC_PINS = [(9, 8), (5, 4)]
    IR_PINS = [3]
    RELAY_PINS = [7]
    SERVO_PINS = [9]


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
    GARBAGE = 500
    PAPER = 1100
    GLASS = 1650
    RECYCLABLES = 2150


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
