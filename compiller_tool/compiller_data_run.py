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
    "SaveA":"E7 02 ",
    "ReturnValue":"E8 02 ",
    "CallElse":"E9 02 ",
    "MathOP":"F0 02 ",
}

# variable -------------------------------

warning_endline = (False, )     # if an line not end by ; } or // in line or the last line
# format: [0]: warning end line ; [1] : line of error ; [2]: module of error ('*' if main module)

not_used_ram = 0    # the number of not used RAM for str value



