from sys import argv
from pathlib import Path

START_ADRESSE = "0400: "

class SmartError(Exception):
    """The error for Smart (syntaxe error)."""
    def __init__(self, message):
        print("Error :")
        self.syntaxerror = message



def compile_smarty(file:str) -> None:
    """Start the compile from file."""

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    FUNCTION_SMA = ("print")

    # -----------

    line_conter = 0

    code_compile = START_ADRESSE


    sma = open(file, "r", encoding="UTF-8")

    code = sma.read()

    code = code.replace("\n", "")
    
    code = code.split(";")

    for line in code:
        if line == "":
            line_conter += 1
    
            continue


        if line[0] in ACUMULATOR_REGISTER:
            line = line.replace(" ", "")
            read_line = line.split("=")
            

            r = read_line[0]
            code_compile += "A9" if r == "A" else "A2" if r == "X" else "A0"

            if len(read_line) != 2:
                raise SmartError(f"smart sintaxe error:\nline {line_conter}")
        
            code_compile += " " + read_line[1] + " "

        else:
            line = line.replace(" ", "")

            function_name, function_arg = line.split(":")
            function_arg = function_arg.split(",")

            if function_name == "print":
                if len(function_arg) != 1:
                    raise SmartError("print function take 1 arg")
                
                if function_arg[0] in ACUMULATOR_REGISTER:
                    if function_arg[0] != "A":
                        raise SmartError(f"print need 'A' registrer, not '{function_arg[0]}'")
                    
                    code_compile += "20 EF FF "
                
                elif function_arg[0][0] == "'":
                    if function_arg[0][2] == "'":
                        char = function_arg[0][1]

                        if char.islower():
                            raise SmartError("char canno't be lower.")
                        
                        code_ascii = ord(char)

                        code_hex = hex(code_ascii)[2:]
                        code_hex = code_hex.upper()

                        code_compile += "A9 " + str(code_hex) + " 20 EF FF "


                    else:
                        raise SmartError("char value need 1 char.")
            


        line_conter += 1
    
    print(code_compile)
    
    Path(argv[1] + ".asm").write_text(code_compile, encoding="UTF-8")

if len(argv) == 1:
    raise Exception("Error : no source was givent")

try:
    compile_smarty(argv[1])
except SmartError as se:
    print(se.syntaxerror)
    