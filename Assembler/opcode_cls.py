# Defines the required data structure for any Opcode


class Opcode:
    def __init__(self, name):
        self.name = name
        self.signals = {}
        self.encoding = []
        self.length = 0
        self.force_padding = False
        self.reads_flags = False
        self.sets_flags = True

# TODO: Move a lot of the parsing logic from token_parser.py to the Opcode class for code clarity and modularity
