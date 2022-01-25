# This class represents a single line of code
from opcode_cls import Opcode
from opcode_map import opcodes as opcode_map
from exceptions import ParseFileError, show_syntax_error
from tokenizer import Token, TokenType
from opcode_map import OperandType
from operand_cls import Operand
import integer_literal as int_l


class Instruction:
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.opcode_token = opcode
        self.operands = operands
        self.operand_list = None
        self.pc_adr = int()

        self._signals = dict()

        self._map_opcode()
        self._map_operands(opcode)

    def check_validity(self) -> bool:
        """Checks if the instruction operands are valid for this instructions Opcode"""
        pass

    def check_completeness(self) -> bool:
        """Checks if the instruction is ready to parse into signals"""
        pass

    def replace_label(self, label: str, pc_address):
        """Replaces any label in the operands with the pc_address"""
        pass

    def get_ram_reads(self) -> list:
        """
        Returns list of integer addresses of any RAM read requests placed by this instruction and -1 if the RAM read
        request is dynamic
        """
        ram_addresses = []
        for i, operand_type in enumerate(self.opcode.encoding):
            if operand_type[0] in [OperandType.RAM_OR_IMM, OperandType.RAM_OR_LABEL, OperandType.RAM_OR_IMM_OR_BOTH]:
                operand = self.operand_list[i]
                if not isinstance(operand, list):
                    operand = [operand]
                ram_address = [int_l.to_number_or_literal(x.text[1:]) for x in operand if x.text.startswith("$")]
                if len(ram_address) > 1:
                    show_syntax_error("Only one $ mem reference allowed per operand", operand)
                elif len(ram_address) == 1:
                    ram_addresses.append(ram_address[0])
        return ram_addresses

    def get_ram_write(self) -> int:
        """
        Return the address of any RAM write requests placed by this instruction and -1 if the RAM write request is
        dynamic
        """
        ram_address = 0
        for i, operand_type in enumerate(self.opcode.encoding):
            if OperandType.WRITE_RAM in operand_type:
                if isinstance(self.operands[i], list):
                    """raise Exception("Invalid Call on Instruction.get_ram_write(): "
                                    "{} in instruction {} is a dynamic RAM call".format(
                        self.operands[i], self.opcode.name))"""
                    ram_address = -1
                else:
                    ram_address =  int_l.to_number_or_literal(self.operands[i].text[1:])
        return ram_address

    def get_signals(self) -> dict:
        """Returns a dictionary of the combinator signals for this instruction"""
        self._signals["copper-ore"] = self.pc_adr
        self._signals.update(self.opcode.signals)
        for i, encode in enumerate(self.opcode.encoding):
            self._signals.update(get_signals_by_operand(self.operand_list[i], encode))
        return self._signals

    def _map_opcode(self):
        """Ensures that self.opcode will be mapped to it's specific opcode based either on inputs of str, Token,
        or the Opcode itself"""
        if isinstance(self.opcode_token, Token):
            self.opcode = opcode_map[self.opcode.text.upper()]()
        elif isinstance(self.opcode_token, str):
            self.opcode = opcode_map[self.opcode.upper()]()
        else:
            error_txt = "Instruction assignment requires opcode input of type str or Token. Was: ", type(
                self.opcode_token)
            raise ParseFileError(error_txt)
        return

    def _map_operands(self, opcode_token: Token):
        """
        Maps the opcodes to the signal encoding and checks for any input errors in the operands
        """
        # So. Problem is we need to determine which operand is a read memory operand and which is a write
        # Any operand that is mapped to "signal-3" is a write ram operation with the STOR opcode being an arbitrary
        # write
        #
        # Any operand that is mapped to "signal-1" or "signal-2" is a read ram operation with the LOAD opcode being an
        # arbitrary read
        #
        # Therefore, it is better to do all the mappings that can be done right away and then resolve labels later

        operands = extract_operands(self.operands)
        if len(operands) != len(self.opcode.encoding):
            show_syntax_error(
                "Incorrect number of operands, was {} but expected {}".format(len(operands), len(self.opcode.encoding)),
                opcode_token)
        self.operand_list = operands
        
        for i, en in enumerate(self.opcode.encoding):
            operand = operands[i]
            if not isinstance(operand, list):
                operand = [operand]
            #check_operand_matches_type(operand, en[0])
            
            
            templist = [i.text for i in operand]
            print(self.opcode.name, " ", templist, " ", en)


def check_operand_matches_type(operands: list, operand_type: OperandType):
    """
    Throws exception if operands have incorrect formatting for a given OperandType
    """
    operand_arrangement = ""
    
    for operand in operands:
        if operand.text.startswith("$"):
            operand_arrangement += "$"
        elif int_l.is_number_or_literal(operand.text):
            operand_arrangement += "N"
        elif operand.t_type in [TokenType.LABEL_NUMERIC, TokenType.LABEL_SYMBOLIC]:
            operand_arrangement += "L"
        else:
            show_syntax_error("Unknown Syntax Error: {} in {} not recognized as a valid operand".format(
                operand.text, operand.file_raw_text), operands[0])
    
    if operand_type == OperandType.IMMEDIATE and operand_arrangement != "N":
        show_syntax_error("Invalid input for Opcode on line: {}. Was expecting number, received: {}".format(
            operands[0].file_raw_text, [x.text for x in operands] 
        ), operands[0])
    elif operand_type == OperandType.WRITE_RAM and operand_arrangement != "$":
        show_syntax_error("Invalid input for Opcode on line: {}. Was expecting memory reference with $, received: "
                          "{}".format(operands[0].file_raw_text, [x.text for x in operands]), operands[0])
    elif operand_type == OperandType.RAM_OR_IMM and operand_arrangement not in ["$", "N"]:
        show_syntax_error("Invalid input: {} Was expecting number literal or memory reference with $, received: "
                          "{}".format(operands[0].file_raw_text, [x.text for x in operands]), operands[0])
    elif operand_type == OperandType.RAM_OR_LABEL and operand_arrangement not in ["$", "L"]:
        show_syntax_error("Invalid input: {} Was expecting number literal or a label, received: "
                          "{}".format(operands[0].file_raw_text, [x.text for x in operands]), operands[0])
    elif operand_type == OperandType.RAM_OR_IMM_OR_BOTH and operand_arrangement not in ["$", "N", "$N"]:
        show_syntax_error("Invalid input: {} Was expecting mem reference followed by number eg [$1, 2], received: "
                          "{}".format(operands[0].file_raw_text, [x.text for x in operands]), operands[0])
    


def get_signals_by_operand(operand, operand_type_w_signals):
    operand_dict = dict()
    operand_type = operand_type_w_signals[0]
    signal_dict = operand_type_w_signals[1]

    if operand_type == OperandType.IMMEDIATE:
        val = immediate_from_operand(operand)
        operand_dict.update(replace_val_in_dict(signal_dict, val))
    elif operand_type == OperandType.WRITE_RAM:
        val = ram_from_operand(operand)
        operand_dict.update(replace_val_in_dict(signal_dict, val))
    elif operand_type in [OperandType.RAM_OR_IMM, OperandType.RAM_OR_LABEL]:
        # label is now a value, so same logic as ram / imm
        # Must see if operand has ram or value
        last_signal_dict = operand_type_w_signals[2]
        if int_l.is_number_or_literal(operand.text):
            val = immediate_from_operand(operand)
            operand_dict.update(replace_val_in_dict(last_signal_dict, val))
        else:
            val = ram_from_operand(operand)
            operand_dict.update(replace_val_in_dict(signal_dict, val))
    elif operand_type == OperandType.RAM_OR_IMM_OR_BOTH:
        # operand is a list, check length
        last_signal_dict = operand_type_w_signals[2]

        if not isinstance(operand, list):
            operand = [operand]

        if len(operand) == 2:
            # both reg and imm
            ram = ram_from_operand(operand[0])
            imm = immediate_from_operand(operand[1])
            operand_dict.update(replace_val_in_dict(signal_dict, ram))
            operand_dict.update(replace_val_in_dict(last_signal_dict, imm))
        elif len(operand) == 1:
            # convert single entry list to token
            if int_l.is_number_or_literal(operand[0].text):
                val = immediate_from_operand(operand[0])
                operand_dict.update(replace_val_in_dict(last_signal_dict, val))
            else:
                val = ram_from_operand(operand[0])
                operand_dict.update(replace_val_in_dict(signal_dict, val))
        else:
            raise Exception("Unknown error: Extracted bracket operand has no length")
            # must check if operand is ram or immediate value

    return operand_dict


def immediate_from_operand(operand):
    val = operand.text
    if not int_l.is_number_or_literal(val):
        show_syntax_error("invalid number {}, must be on format [-][0x|0b]nnnn".format(val), operand)
    num = int_l.to_number_or_literal(val)
    if not int_l.verify_number_range(num):
        show_syntax_error("Immediate number outside signed 32-bit range. Must be within -2^31..2^31 -1. Was: " + num,
                          operand)
    return num


def ram_from_operand(operand):
    val = operand.text
    if not (val.startswith("$")):
        show_syntax_error("Memory must be referenced with $ " + val, operand)
    return int_l.to_number_or_literal(val[1:])


def replace_val_in_dict(sym_d, val):
    for key in sym_d:
        if sym_d[key] == "var":
            sym_d[key] = val
    return sym_d


def extract_operands(operand_tokens):
    """
    Takes in a list of tokens, and extracts the operands
    Brackets are grouped as a list.
    """
    result = list()
    active_bracket_group = None
    for t in operand_tokens:
        if t.text == "[":
            if active_bracket_group is not None:
                show_syntax_error("Can't open a bracket within another bracket.", t)
            active_bracket_group = list()
        elif t.text == "]":
            if len(active_bracket_group) == 0:
                show_syntax_error("Invalid content in bracket group", t)
            result.append(active_bracket_group)
            active_bracket_group = None
        elif t.text == ",":
            continue
        else:
            if active_bracket_group is not None:
                # append to bracket group
                active_bracket_group.append(t)
            else:
                result.append(t)
    if active_bracket_group is not None:
        t = operand_tokens[-1]
        show_syntax_error("Did not close bracket", t)
    return result
