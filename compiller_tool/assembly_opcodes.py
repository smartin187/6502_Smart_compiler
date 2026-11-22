# -*- coding: utf-8 -*-

"""
The opcodes for the compiler.
"""

PLATFORM = "6502"

class Mode:
    ABS = "absolute"
    IMM = "immediate"

class OpCodes:
    """
    The OP codes for the compiler. For some methods, use the parameter `mode` for select the mode (default is immediate).
    """

    def LDA(mode=Mode.IMM):
        match PLATFORM:
            case "6502":
                return "A9" if mode == Mode.IMM else "AD"

