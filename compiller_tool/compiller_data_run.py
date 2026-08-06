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
    "CallElse":"02 00 ",
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

# variable -------------------------------

warning_endline = (False, )     # if an line not end by ; } or // in line or the last line
# format: [0]: warning end line ; [1] : line of error ; [2]: module of error ('*' if main module)

not_used_ram = 0    # the number of not used RAM for str value

need_error = False   # if need runtime error

double_space_error = False # if an double space on code is detected.

