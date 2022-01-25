# label class and label related functions

from exceptions import ParseFileError, AsmSyntaxError


class NumericLabel:
    """A numeric label is a single digit label from the range 0 to 9. It is a local label."""
    def __init__(self, digit, inst_index, file_line_number):
        self.digit = digit
        self.inst_index = inst_index
        self.was_referenced = False
        self.file_line_number = file_line_number


def find_numeric_labels(labels, digit, pc_adr):
    """
    Linear search through list of numeric labels.
    List is assumed to be sorted by PC address.
    """
    # Note to self: Might implement binary search if better performance is required
    result = dict()
    back = None
    forward = None
    prev_label = None
    for label in labels:
        assert isinstance(label, NumericLabel)
        if label.digit == digit:
            if prev_label is not None and prev_label.inst_index > label.inst_index:
                error_txt = "List of numeric labels not in order (by address). " \
                            "Previous: [{}: {}], current: [{}: {}]" \
                            .format(prev_label.digit, prev_label.inst_index, label.digit, label.inst_index)
                raise ParseFileError(error_txt)

            if label.inst_index <= pc_adr:
                back = label
            else:
                forward = label
                break
            prev_label = label
    result["back"] = back
    result["forward"] = forward
    return result


def find_forward_label(labels, digit, pc_adr):
    forward = find_numeric_labels(labels, digit, pc_adr)["forward"]
    if forward is None:
        raise AsmSyntaxError("No forward label found.")
    return forward


def find_back_label(labels, digit, pc_adr):
    back = find_numeric_labels(labels, digit, pc_adr)["back"]
    if back is None:
        raise AsmSyntaxError("No back label found.")
    return back


def is_numeric_label(text: str) -> bool:
    return len(text) == 1 and text.isdecimal()
