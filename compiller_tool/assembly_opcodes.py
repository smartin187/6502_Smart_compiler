# -*- coding: utf-8 -*-

"""
The opcodes for the compiler.
"""

PLATFORM = "6502"

class Mode:
    ABS = "absolute"
    IMM = "immediate"
    IND = "indirect"
    ZP = "zero_page"
    ZPX = "zero_page_x"
    ZPY = "zero_page_y"
    ABSX = "absolute_x"
    ABSY = "absolute_y"
    INDX = "indirect_x"
    INDY = "indirect_y"
    ACC = "accumulator"
    REL = "relative"
    IMP = "implied"

class Platforms:
    _6502 = "6502"

class Hex:
    """
    The OP codes for the compiler. For some methods, use the parameter `mode` for select the mode (default is immediate).
    """

    def ADC(mode: str=Mode.IMM) -> str:
        """ADC instruction (add with carry)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "69", Mode.ZP: "65", Mode.ZPX: "75", Mode.ABS: "6D",
                        Mode.ABSX: "7D", Mode.ABSY: "79", Mode.INDX: "61", Mode.INDY: "71"}[mode]

    def AND(mode: str=Mode.IMM) -> str:
        """AND instruction (bitwise AND with accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "29", Mode.ZP: "25", Mode.ZPX: "35", Mode.ABS: "2D",
                        Mode.ABSX: "3D", Mode.ABSY: "39", Mode.INDX: "21", Mode.INDY: "31"}[mode]

    def ASL(mode: str=Mode.ACC) -> str:
        """ASL instruction (arithmetic shift left)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ACC: "0A", Mode.ZP: "06", Mode.ZPX: "16", Mode.ABS: "0E", Mode.ABSX: "1E"}[mode]

    def BCC(mode: str=Mode.REL) -> str:
        """BCC instruction (branch on carry clear)."""
        match PLATFORM:
            case Platforms._6502:
                return "90"

    def BCS(mode: str=Mode.REL) -> str:
        """BCS instruction (branch on carry set)."""
        match PLATFORM:
            case Platforms._6502:
                return "B0"

    def BEQ(mode: str=Mode.REL) -> str:
        """BEQ instruction (branch on equal)."""
        match PLATFORM:
            case Platforms._6502:
                return "F0"

    def BIT(mode: str=Mode.ZP) -> str:
        """BIT instruction (test bits)."""
        match PLATFORM:
            case Platforms._6502:
                return "24" if mode == Mode.ZP else "2C"

    def BMI(mode: str=Mode.REL) -> str:
        """BMI instruction (branch on minus)."""
        match PLATFORM:
            case Platforms._6502:
                return "30"

    def BNE(mode: str=Mode.REL) -> str:
        """BNE instruction (branch on not equal)."""
        match PLATFORM:
            case Platforms._6502:
                return "D0"

    def BPL(mode: str=Mode.REL) -> str:
        """BPL instruction (branch on plus)."""
        match PLATFORM:
            case Platforms._6502:
                return "10"

    def BRK(mode: str=Mode.IMP) -> str:
        """BRK instruction (break)."""
        match PLATFORM:
            case Platforms._6502:
                return "00"

    def BVC(mode: str=Mode.REL) -> str:
        """BVC instruction (branch on overflow clear)."""
        match PLATFORM:
            case Platforms._6502:
                return "50"

    def BVS(mode: str=Mode.REL) -> str:
        """BVS instruction (branch on overflow set)."""
        match PLATFORM:
            case Platforms._6502:
                return "70"

    def CLC(mode: str=Mode.IMP) -> str:
        """CLC instruction (clear carry)."""
        match PLATFORM:
            case Platforms._6502:
                return "18"

    def CLD(mode: str=Mode.IMP) -> str:
        """CLD instruction (clear decimal)."""
        match PLATFORM:
            case Platforms._6502:
                return "D8"

    def CLI(mode: str=Mode.IMP) -> str:
        """CLI instruction (clear interrupt disable)."""
        match PLATFORM:
            case Platforms._6502:
                return "58"

    def CLV(mode: str=Mode.IMP) -> str:
        """CLV instruction (clear overflow)."""
        match PLATFORM:
            case Platforms._6502:
                return "B8"

    def CMP(mode: str=Mode.IMM) -> str:
        """CMP instruction (compare accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "C9", Mode.ZP: "C5", Mode.ZPX: "D5", Mode.ABS: "CD",
                        Mode.ABSX: "DD", Mode.ABSY: "D9", Mode.INDX: "C1", Mode.INDY: "D1"}[mode]

    def CPX(mode: str=Mode.IMM) -> str:
        """CPX instruction (compare X register)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "E0", Mode.ZP: "E4", Mode.ABS: "EC"}[mode]

    def CPY(mode: str=Mode.IMM) -> str:
        """CPY instruction (compare Y register)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "C0", Mode.ZP: "C4", Mode.ABS: "CC"}[mode]

    def DEC(mode: str=Mode.ZP) -> str:
        """DEC instruction (decrement memory)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ZP: "C6", Mode.ZPX: "D6", Mode.ABS: "CE", Mode.ABSX: "DE"}[mode]

    def DEX(mode: str=Mode.IMP) -> str:
        """DEX instruction (decrement X register)."""
        match PLATFORM:
            case Platforms._6502:
                return "CA"

    def DEY(mode: str=Mode.IMP) -> str:
        """DEY instruction (decrement Y register)."""
        match PLATFORM:
            case Platforms._6502:
                return "88"

    def EOR(mode: str=Mode.IMM) -> str:
        """EOR instruction (bitwise exclusive OR)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "49", Mode.ZP: "45", Mode.ZPX: "55", Mode.ABS: "4D",
                        Mode.ABSX: "5D", Mode.ABSY: "59", Mode.INDX: "41", Mode.INDY: "51"}[mode]

    def INC(mode: str=Mode.ZP) -> str:
        """INC instruction (increment memory)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ZP: "E6", Mode.ZPX: "F6", Mode.ABS: "EE", Mode.ABSX: "FE"}[mode]

    def INX(mode: str=Mode.IMP) -> str:
        """INX instruction (increment X register)."""
        match PLATFORM:
            case Platforms._6502:
                return "E8"

    def INY(mode: str=Mode.IMP) -> str:
        """INY instruction (increment Y register)."""
        match PLATFORM:
            case Platforms._6502:
                return "C8"

    def JMP(mode: str=Mode.ABS) -> str:
        """JMP instruction (jump)."""
        match PLATFORM:
            case Platforms._6502:
                return "4C" if mode == Mode.ABS else "6C"

    def JSR(mode: str=Mode.ABS) -> str:
        """JSR instruction (jump to subroutine)."""
        match PLATFORM:
            case Platforms._6502:
                return "20"

    def LDA(mode: str=Mode.IMM) -> str:
        """LDA instruction (load accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "A9", Mode.ZP: "A5", Mode.ZPX: "B5", Mode.ABS: "AD",
                        Mode.ABSX: "BD", Mode.ABSY: "B9", Mode.INDX: "A1", Mode.INDY: "B1"}[mode]

    def LDX(mode: str=Mode.IMM) -> str:
        """LDX instruction (load X register)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "A2", Mode.ZP: "A6", Mode.ZPY: "B6", Mode.ABS: "AE", Mode.ABSY: "BE"}[mode]

    def LDY(mode: str=Mode.IMM) -> str:
        """LDY instruction (load Y register)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "A0", Mode.ZP: "A4", Mode.ZPX: "B4", Mode.ABS: "AC", Mode.ABSX: "BC"}[mode]

    def LSR(mode: str=Mode.ACC) -> str:
        """LSR instruction (logical shift right)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ACC: "4A", Mode.ZP: "46", Mode.ZPX: "56", Mode.ABS: "4E", Mode.ABSX: "5E"}[mode]

    def NOP(mode: str=Mode.IMP) -> str:
        """NOP instruction (no operation)."""
        match PLATFORM:
            case Platforms._6502:
                return "EA"

    def ORA(mode: str=Mode.IMM) -> str:
        """ORA instruction (bitwise OR with accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "09", Mode.ZP: "05", Mode.ZPX: "15", Mode.ABS: "0D",
                        Mode.ABSX: "1D", Mode.ABSY: "19", Mode.INDX: "01", Mode.INDY: "11"}[mode]

    def PHA(mode: str=Mode.IMP) -> str:
        """PHA instruction (push accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return "48"

    def PHP(mode: str=Mode.IMP) -> str:
        """PHP instruction (push processor status)."""
        match PLATFORM:
            case Platforms._6502:
                return "08"

    def PLA(mode: str=Mode.IMP) -> str:
        """PLA instruction (pull accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return "68"

    def PLP(mode: str=Mode.IMP) -> str:
        """PLP instruction (pull processor status)."""
        match PLATFORM:
            case Platforms._6502:
                return "28"

    def ROL(mode: str=Mode.ACC) -> str:
        """ROL instruction (rotate left)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ACC: "2A", Mode.ZP: "26", Mode.ZPX: "36", Mode.ABS: "2E", Mode.ABSX: "3E"}[mode]

    def ROR(mode: str=Mode.ACC) -> str:
        """ROR instruction (rotate right)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ACC: "6A", Mode.ZP: "66", Mode.ZPX: "76", Mode.ABS: "6E", Mode.ABSX: "7E"}[mode]

    def RTI(mode: str=Mode.IMP) -> str:
        """RTI instruction (return from interrupt)."""
        match PLATFORM:
            case Platforms._6502:
                return "40"

    def RTS(mode: str=Mode.IMP) -> str:
        """RTS instruction (return from subroutine)."""
        match PLATFORM:
            case Platforms._6502:
                return "60"

    def SBC(mode: str=Mode.IMM) -> str:
        """SBC instruction (subtract with carry)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.IMM: "E9", Mode.ZP: "E5", Mode.ZPX: "F5", Mode.ABS: "ED",
                        Mode.ABSX: "FD", Mode.ABSY: "F9", Mode.INDX: "E1", Mode.INDY: "F1"}[mode]

    def SEC(mode: str=Mode.IMP) -> str:
        """SEC instruction (set carry)."""
        match PLATFORM:
            case Platforms._6502:
                return "38"

    def SED(mode: str=Mode.IMP) -> str:
        """SED instruction (set decimal)."""
        match PLATFORM:
            case Platforms._6502:
                return "F8"

    def SEI(mode: str=Mode.IMP) -> str:
        """SEI instruction (set interrupt disable)."""
        match PLATFORM:
            case Platforms._6502:
                return "78"

    def STA(mode: str=Mode.ZP) -> str:
        """STA instruction (store accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ZP: "85", Mode.ZPX: "95", Mode.ABS: "8D", Mode.ABSX: "9D",
                        Mode.ABSY: "99", Mode.INDX: "81", Mode.INDY: "91"}[mode]

    def STX(mode: str=Mode.ZP) -> str:
        """STX instruction (store X register)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ZP: "86", Mode.ZPY: "96", Mode.ABS: "8E"}[mode]

    def STY(mode: str=Mode.ZP) -> str:
        """STY instruction (store Y register)."""
        match PLATFORM:
            case Platforms._6502:
                return {Mode.ZP: "84", Mode.ZPX: "94", Mode.ABS: "8C"}[mode]

    def TAX(mode: str=Mode.IMP) -> str:
        """TAX instruction (transfer accumulator to X)."""
        match PLATFORM:
            case Platforms._6502:
                return "AA"

    def TAY(mode: str=Mode.IMP) -> str:
        """TAY instruction (transfer accumulator to Y)."""
        match PLATFORM:
            case Platforms._6502:
                return "A8"

    def TSX(mode: str=Mode.IMP) -> str:
        """TSX instruction (transfer stack pointer to X)."""
        match PLATFORM:
            case Platforms._6502:
                return "BA"

    def TXA(mode: str=Mode.IMP) -> str:
        """TXA instruction (transfer X to accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return "8A"

    def TXS(mode: str=Mode.IMP) -> str:
        """TXS instruction (transfer X to stack pointer)."""
        match PLATFORM:
            case Platforms._6502:
                return "9A"

    def TYA(mode: str=Mode.IMP) -> str:
        """TYA instruction (transfer Y to accumulator)."""
        match PLATFORM:
            case Platforms._6502:
                return "98"


