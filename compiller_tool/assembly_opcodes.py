# -*- coding: utf-8 -*-

"""
The opcodes for the compiler.
"""

PLATFORM = "6502"

class Mode:
    ABS = "absolute"
    IMM = "immediate"
    IND = "indirect"

class Platforms:
    _6502 = "6502"

class Hex:
    """
    The OP codes for the compiler. For some methods, use the parameter `mode` for select the mode (default is immediate).
    """

    def LDA(mode: str=Mode.IMM) -> str:
        """LDA instruction (load accumulator). Default mode is immediate."""
        match PLATFORM:
            case Platforms._6502:
                return "A9" if mode == Mode.IMM else "AD"
    
    def BNE() -> str:
        """BNE instruction (branche if not equal). They are node mod for this instruction."""
        match PLATFORM:
            case Platforms._6502:
                return "D0"

    def JMP(mode: str=Mode.ABS) -> str:
        """JMP instruction. Default mode is absolute"""
        match PLATFORM:
            case Platforms._6502:
                return "4C" if mode == Mode.ABS else "6C"


