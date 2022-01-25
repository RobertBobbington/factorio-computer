# The different operand types

from enum import Enum, auto


class OperandType(Enum):
    WRITE_RAM = auto()
    IMMEDIATE = auto()
    RAM_OR_IMM_OR_BOTH = auto()
    RAM_OR_IMM = auto()
    RAM_OR_LABEL = auto()
