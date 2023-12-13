from enum import StrEnum, auto


class Layer(StrEnum):

    STAGING = auto()
    INTERMEDIATE = auto()
    MARTS = auto()