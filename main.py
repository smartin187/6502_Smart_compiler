from sys import argv
from pathlib import Path
import os
import traceback

START_ADRESSE = "0400: "
CODE_ADRESSE = 1024

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

    def good_hex(code:str) -> bool:
        """Return True if the hex value is good, False else."""
        try:
            int(code, base=16)
        except:
            return False
        else:
            return True if len(code) == 2 else False
        
    def control_hex(code:str) -> None:
        """If good_hex return False, raise SmartError."""
        if not good_hex(code):
            raise SmartError(f"Bad hex value '{code}'")

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    # -----------

    smart_var = {}
    adress_var = 0x300

    line_conter = 0

    code_compile = START_ADRESSE

    go_to = {}

    adress_conter = 0


    sma = open(file, "r", encoding="UTF-8")

    code_start = sma.read()

    sma.close()

    code_line = code_start.split("\n")

    code = ""

    for line in code_line:
        code += line.split("//")[0] + "\n"
    

    code = code.replace("\n", "").replace(" ", "").split(";")

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
                control_hex(read_line[1])
                code_compile += " " + read_line[1] + " "
            
            elif read_line[1][0] == "'":
                code_compile += " " + get_char(read_line[1]) + " "
            
            else:
                raise SmartError(f"Smart value error:\nline {line_conter}")

            adress_conter += 2

        elif line[0] == "#":
            name = line[1:]

            if (" " in name or "\n" in name) or (name in ACUMULATOR_REGISTER):
                raise SmartError(f"Invalid name for goto : '{name}'")

            hex_adress = hex(CODE_ADRESSE + adress_conter)[2:]

            
            hex_adress = "0" * (4-len(hex_adress)) + hex_adress


            go_to[name] = hex_adress

        
        elif line.startswith("."):      # variable
            
            line = line.replace(" ", "")[1:]

            var_name, value = line.split("=")

            if var_name not in smart_var: # make new variable
                if len(smart_var) >= 256:
                    raise SmartError("Memory error : maximum variable are 256.")
                smart_var[var_name] = adress_var
                adress_var += 1
            
            control_hex(value)
            
            adress_RAM = hex(smart_var[var_name])[2:]

            adress_RAM = "0" * (4 - len(adress_RAM)) + adress_RAM

            adress_RAM = adress_RAM[2:] + " " + adress_RAM[:2]
            
            code_compile += f"A9 {value} 8D {adress_RAM} "

            adress_conter += 5

        else:     # function

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

                    adress_conter += 3
                
                elif function_arg[0][0] == "'":
                    code_compile += "A9 " + str(get_char(function_arg[0])) + " 20 EF FF "

                    adress_conter += 5
                
                elif function_arg[0][0] == "\"":
                    smart_str = function_arg[0]

                    if smart_str[-1] != "\"":
                        raise SmartError(f"str value was not closed.")
                    
                    for char in smart_str[1:-1]:
                        code_compile += "A9 " + get_char(f"'{char}'") + " 20 EF FF "

                        adress_conter += 5

                else:
                    control_hex(function_arg[0])

                    code_compile += "A9 " + function_arg[0] + " 20 EF FF "

                    adress_conter += 5



            elif function_name == "quit":
                if function_arg != [""]:
                    raise SmartError(f"Function 'quit' not take arg.")
                
                code_compile += "00 "
            
            elif function_name == "goto":
                if len(function_arg) != 1:
                    raise SmartError("Function 'goto' take 1 arg.")
                
                name = function_arg[0]

                try:
                    adress = go_to[name]
                
                except KeyError:
                    raise SmartError(f"'{name}' is not defined for goto !")

                code_compile += f"4C {adress[2:]} {adress[:2]} "

            
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
    print(traceback.format_exc())