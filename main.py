from sys import argv
from pathlib import Path
import os

START_ADRESSE = "0400: "

class SmartError(Exception):
    """The error for Smart (syntaxe error)."""
    def __init__(self, message):
        print("Error :")
        self.syntaxerror = message



def compile_smarty(file:str) -> None:
    """Start the compile from file."""
    def get_char(char_type:str) -> str:
        """Return the char value of Smart."""
        if char_type[2] == "'":
            char = char_type[1]

            if char.islower():
                raise SmartError("char canno't be lower.")
            
            code_ascii = ord(char)

            code_hex = hex(code_ascii)[2:]
            code_hex = code_hex.upper()
            return code_hex

        else:
            raise SmartError("char value need 1 char.")

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    FUNCTION_SMA = ("print")

    # -----------

    line_conter = 0

    code_compile = START_ADRESSE


    sma = open(file, "r", encoding="UTF-8")

    code = sma.read()

    sma.close()

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
                raise SmartError(f"Smart syntaxe error:\nline {line_conter}")
        
            if len(read_line[1]) == 2:
                code_compile += " " + read_line[1] + " "
            
            elif read_line[1][0] == "'":
                code_compile += " " + get_char(read_line[1]) + " "
            
            else:
                raise SmartError(f"Smart value error:\nline {line_conter}")

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
                    code_compile += "A9 " + str(get_char(function_arg[0])) + " 20 EF FF "
                
                elif function_arg[0][0] == "\"":
                    smart_str = function_arg[0]

                    if smart_str[-1] != "\"":
                        raise SmartError(f"str value was not closed.")
                    
                    for char in smart_str[1:-1]:
                        code_compile += "A9 " + get_char(f"'{char}'") + " 20 EF FF "

            elif function_name == "quit":
                if function_arg != [""]:
                    raise SmartError(f"Function 'quit' not take arg.")
                
                code_compile += "00 "
            
            else:
                raise SmartError(f"Function '{function_name}' not exist.")


        line_conter += 1
    
    code_compile += "00"
    
    print(code_compile)
    
    Path(os.path.splitext(argv[1])[0] + ".asm").write_text(code_compile, encoding="UTF-8")

if len(argv) == 1:
    raise Exception("Error : no source was givent")

try:
    compile_smarty(argv[1])
except SmartError as se:
    print(se.syntaxerror)

except:
    print("Error during build")