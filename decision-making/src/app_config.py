from enum import Enum, unique
import logging

logging.basicConfig(format='[%(asctime)s_%(levelname)s] %(name)s_%(module)s: %(message)s', level=logging.DEBUG)


@unique
class Thresholds(int, Enum):
    INDUCTIVE_SENSOR = 1
    CAPACITIVE_SENSOR = 1
    WEIGHT = 100


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


class Waste:
    def __init__(self):
        self.type = Classification.UNKNOWN
        self.status = Status.IN_PROGRESS
        self.step = None
        self.failure_messages = []
        self.workflow = {}
