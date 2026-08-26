# -*- coding: utf-8 -*-

"""
Have data during the compilation.
Have constantes for the adress.

Have:
- warning_endline: tuple for know if they are a warning if a line not end with ';'.
- the number of adress reserved for str value.
"""

# constent -------------------------------

SYS_ADRESS = {
    "SaveA":"00 00 ",
    "ReturnValue":"01 00 ",
    #"CallElse":"02 00 ",    # obsolette ! To remove
    "MathOP":"03 00 ",
    "SaveStr":"04 00 ",     # SaveStr start at EB 00 and have a len of 21 (end at 0x19 00)
    "SaveStrCMP":"19 00 ",  # SaveStrCMP start at 0x19 00 and have a len of 21 (end at 0x32 00) - Used to save a str for compare (if, ==...)
    "SaveAToIndex":"32 00 ",   # SaveAToIndex start at 0x32 00
}

SMART_ERRORS = {     # the code error for Smart
    "Index out of range": "I",
    "Division by zero": "/"
}

# placeholder with double space
SMART_PLACEHOLDER = (
    "!  smart_input",
    "!  smart_runtime_error"
)

BASE_ALLOW_CHAR = "!\"#$%'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_ "   # the allowed char without \n and \r

ALLOW_CHAR = BASE_ALLOW_CHAR + "\n\r"

MAX_VARIABLE_CREATED = 256  # the maximum number of bytes for variable.

START_ADRESS_VAR = 0x300

# base value -------------------------------

_WARNING_ENDLINE = (False, )     # if an line not end by ; } or // in line or the last line
# format: [0]: warning end line ; [1] : line of error ; [2]: module of error ('*' if main module)

_NOT_USED_RAM = 0    # the number of not used RAM for str value

_NEED_ERROR = False   # if need runtime error

_DOUBLE_SPACE_ERROR = False # if an double space on code is detected.

_NOT_USED_CALL_ELSE = 0

_DEBUG_MAX = False  # if the debug is True, on the binary the line running is print.

# -------------------------------

_define_dict = None

def reset_define(define_dict:dict) -> None:
    """Add the define_dict to reset_data"""
    global _define_dict
    _define_dict = define_dict

def reset_data() -> None:
    """Reset the data.
    Used for test.py (because tests are run one after the other)."""
    global warning_endline, not_used_ram, need_error, double_space_error, not_used_call_else, debug_max
    warning_endline = _WARNING_ENDLINE
    not_used_ram = _NOT_USED_RAM
    need_error = _NEED_ERROR
    double_space_error = _DOUBLE_SPACE_ERROR
    not_used_call_else = _NOT_USED_CALL_ELSE
    debug_max = _DEBUG_MAX

    # reset value of compiletime keyword
    _define_dict.clear()

# variable -------------------------------

warning_endline = _WARNING_ENDLINE

not_used_call_else = _NOT_USED_CALL_ELSE

not_used_ram = _NOT_USED_RAM

need_error = _NEED_ERROR

double_space_error = _DOUBLE_SPACE_ERROR

debug_max = _DEBUG_MAX
