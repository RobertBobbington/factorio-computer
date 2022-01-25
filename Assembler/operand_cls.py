
from operand_type import OperandType
from tokenizer import Token


class Operand:
    def __init__(self, operand_type: OperandType, operand_token: Token, signals: dict):
        self.operand_type = operand_type
        self.operand_token = operand_token
        self.signals = signals
