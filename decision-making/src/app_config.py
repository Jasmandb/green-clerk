from enum import Enum, unique


@unique
class Classification(str, Enum):
    WASTE = 'WASTE'
    PAPER = 'THRESHOLD'
    GLASS = 'EMPTY'
    METAL = 'METAL'
    RECYCLABLES = 'RECYCLABLES'
    UNKNOWN = 'UNKNOWN'


@unique
class BinLevel(str, Enum):
    FULL = 'FULL'
    THRESHOLD = 'THRESHOLD'
    EMPTY = 'EMPTY'


@unique
class Tasks(str, Enum):
    CLASSIFY = 'CLASSIFY'
