from sys import argv

def compile_smarty(file:str) -> None:
    """Start the compile from file."""

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    # -----------

    line_conter = 0

    code_compile = ""


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
    
        line_conter += 1
    
    print(code_compile)

if len(argv) == 1:
    raise Exception("Error : no source was givent")


compile_smarty(argv[1])

    