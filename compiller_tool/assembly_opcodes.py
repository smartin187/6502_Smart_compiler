# -*- coding: utf-8 -*-

"""
The opcodes for the compiler.
"""

PLATFORM = "6502"

class Mode:
    ABS = "absolute"
    IMM = "immediate"

class Platforms:
    _6502 = "6502"

class Hex:
    """
    The OP codes for the compiler. For some methods, use the parameter `mode` for select the mode (default is immediate).
    """

    def LDA(mode=Mode.IMM):
        match PLATFORM:
            case Platforms._6502:
                return "A9" if mode == Mode.IMM else "AD"
    
    def BNE():
        match PLATFORM:
            case Platforms._6502:
                return "D0"

