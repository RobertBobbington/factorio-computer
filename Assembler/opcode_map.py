# all opcodes and their signals are programmed here

from collections import OrderedDict
from operand_type import OperandType
from opcode_cls import Opcode

opcodes = OrderedDict()


def tag(opcode):
    """Add function to opcode map"""
    return lambda func: opcodes.setdefault(opcode.upper(), func)


@tag("HLT")
def hlt_inst():
    opcd = Opcode("HLT")
    opcd.signals = {"signal-O": 6}
    opcd.encoding = []
    opcd.length = 5
    opcd.force_padding = True
    opcd.sets_flags = False
    return opcd


@tag("HLTG")
def hltg_inst():
    opcd = Opcode("HLTG")
    opcd.signals = {"signal-O": 6, "signal-A": 1}
    opcd.encoding = []
    opcd.length = 5
    opcd.force_padding = True
    opcd.sets_flags = False
    return opcd


@tag("HLTB")
def opcodeb_inst():
    opcd = Opcode("HLTB")
    opcd.signals = {"signal-O": 6, "signal-A": 2}
    opcd.encoding = []
    opcd.length = 5
    opcd.force_padding = True
    opcd.sets_flags = False
    return opcd


# TODO: Implement NOP instruction as an assembler only instruction
"""
@tag("NOP")
def nop_inst():
    instr_tick_count = 1
    return signals, [], instr_tick_count
"""


@tag("STOR")
def stor_inst():
    opcd = Opcode("STOR")
    opcd.signals = {"signal-O": 1}
    opcd.encoding = [
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = True
    return opcd


@tag("LOAD")
def load_inst():
    opcd = Opcode("LOAD")
    opcd.signals = {"signal-O": 2}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}]
    ]
    opcd.length = 6
    opcd.force_padding = True
    return opcd


@tag("B")
def b_inst():
    opcd = Opcode("B")
    opcd.signals = {"signal-O": 3}
    opcd.encoding = [
        [OperandType.RAM_OR_LABEL,
         {"signal-1": "var"}, {"signal-A": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = True
    opcd.reads_flags = True
    opcd.sets_flags = False
    return opcd


@tag("BZ")
def bz_inst():
    opcd = Opcode("BZ")
    opcd.signals = {"signal-O": 4}
    opcd.encoding = [
        [OperandType.RAM_OR_LABEL,
         {"signal-1": "var"}, {"signal-A": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = True
    opcd.reads_flags = True
    opcd.sets_flags = False
    return opcd


@tag("BN")
def bn_inst():
    opcd = Opcode("BN")
    opcd.signals = {"signal-O": 5}
    opcd.encoding = [
        [OperandType.RAM_OR_LABEL,
         {"signal-1": "var"}, {"signal-A": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = True
    opcd.reads_flags = True
    opcd.sets_flags = False
    return opcd


# TODO Create builtin macro that clears Memory
"""
@tag("CMEM")
def cmem_inst():
    signals = {"copper-plate": 12, "signal-grey": 1, "signal-black": 1}
    return signals, []
"""


@tag("ADD")
def add_inst():
    opcd = Opcode("ADD")
    opcd.signals = {"signal-O": 10}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("SUB")
def sub_inst():
    opcd = Opcode("SUB")
    opcd.signals = {"signal-O": 11}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("CMP")
def cmp_inst():
    opcd = Opcode("CMP")
    opcd.signals = {"signal-O": 11, "signal-3": -1}
    opcd.encoding = [
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = True
    return opcd


@tag("TST")
def tst_inst():
    opcd = Opcode("TST")
    opcd.signals = {"signal-O": 10, "signal-2": 0, "signal-3": -1}
    opcd.encoding = [
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("MUL")
def mul_inst():
    opcd = Opcode("MUL")
    opcd.signals = {"signal-O": 12}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("DIV")
def div_inst():
    opcd = Opcode("DIV")
    opcd.signals = {"signal-O": 13}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("MOD")
def mod_inst():
    opcd = Opcode("MOD")
    opcd.signals = {"signal-O": 14}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("POW")
def pow_inst():
    opcd = Opcode("POW")
    opcd.signals = {"signal-O": 15}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("SAL")
def sal_inst():
    opcd = Opcode("SAL")
    opcd.signals = {"signal-O": 16}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("SAR")
def sar_inst():
    opcd = Opcode("SAR")
    opcd.signals = {"signal-O": 17}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


# NOT x = -x-1
@tag("NOT")
def not_inst():
    opcd = Opcode("NOT")
    opcd.signals = {"signal-O": 11, "signal-A": -1}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("AND")
def and_inst():
    opcd = Opcode("AND")
    opcd.signals = {"signal-O": 18}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("OR")
def or_inst():
    opcd = Opcode("OR")
    opcd.signals = {"signal-O": 19}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("XOR")
def xor_inst():
    opcd = Opcode("XOR")
    opcd.signals = {"signal-O": 20}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-1": "var"}, {"signal-A": "var"}],
        [OperandType.RAM_OR_IMM_OR_BOTH,
         {"signal-2": "var"}, {"signal-B": "var"}]
    ]
    opcd.length = 5
    opcd.force_padding = False
    return opcd


@tag("PC")
def xor_inst():
    opcd = Opcode("PC")
    opcd.signals = {"signal-O": 21}
    opcd.encoding = [
        [OperandType.WRITE_RAM,
         {"signal-3": "var"}],
    ]
    opcd.length = 4
    opcd.force_padding = False
    return opcd
