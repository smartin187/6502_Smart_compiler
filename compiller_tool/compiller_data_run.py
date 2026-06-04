# -*- coding: utf-8 -*-

"""
Have data during the compilation.

Have:
- warning_endline: tuple for know if they are a warning if a line not end with ';'.
"""

warning_endline = (False, )     # if an line not end by ; } or // in line or the last line
# format: [0]: warning end line ; [1] : line of error ; [2]: module of error ('*' if main module)