# takes a list of instructions and generates list of signals for the constant combinators PROM


import integer_literal as int_l
from exceptions import show_syntax_error, show_warning_one_line
from instruction import Instruction
from opcode_map import opcodes
from operand_type import OperandType


def inst_to_signals(instructions):
    const_comb_signals = list()

    for inst in instructions:
        assert isinstance(inst, Instruction)
        opcode = inst.opcode.text
        if opcode.upper() not in opcodes:
            show_syntax_error("Unknown opcode {}".format(opcode), inst.opcode)

        control_signals = opcodes[opcode.upper()]().signals
        encoding = opcodes[opcode.upper()]().encoding

        instruction_signals = iterate_operands(inst, control_signals, encoding)
        instruction_signals["copper-ore"] = inst.pc_adr

        const_comb_signals.append(instruction_signals)

    return const_comb_signals


def iterate_operands(inst: Instruction, sig_dict, encoding):
    result_signals = dict()
    result_signals.update(sig_dict)
    operands = extract_operands(inst.operands)
    if len(operands) != len(encoding):
        t = inst.opcode
        show_syntax_error("Incorrect number of operands, was {} but expected {}".format(len(operands), len(encoding)),
                          t)
    for i, e in enumerate(operands):
        operand_signals = get_signals_by_operand(e, encoding[i])
        result_signals.update(operand_signals)
    return result_signals


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
    if not(val.startswith("$")):
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
