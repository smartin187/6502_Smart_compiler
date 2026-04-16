from sys import argv
from pathlib import Path

START_ADRESSE = "0400: "

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
                raise Exception(f"smart sintaxe error:\nline {line_conter}")
        
            code_compile += " " + read_line[1] + " "

        else:
            line = line.replace(" ", "")

            function_name, function_arg = line.split(":")
            function_arg = function_arg.split(",")

            if function_name == "print":
                if len(function_arg) != 1:
                    raise Exception("print function take 1 arg")
                
                if function_arg[0] in ACUMULATOR_REGISTER:
                    if function_arg[0] != "A":
                        raise Exception(f"print need 'A' registrer, not '{function_arg[0]}'")
                    
                    code_compile += "20 EF FF "
            


        line_conter += 1
    
    print(code_compile)
    
    Path(argv[1] + ".asm").write_text(code_compile, encoding="UTF-8")

if len(argv) == 1:
    raise Exception("Error : no source was givent")


compile_smarty(argv[1])

    