# -*- coding: utf-8 -*-

"""
The compiller for smart.

Fonction: compile_smarty for start the compile of a smart code.
"""

from pathlib import Path
import os
import logging

os.system('color')

logging.basicConfig(format="SmartCompiller %(levelname)s: %(message)s", level=logging.INFO)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',
        'INFO': '\033[32m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[31m',
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)

for handler in logging.root.handlers:
    handler.setFormatter(ColoredFormatter('SmartCompiller %(levelname)s: %(message)s'))


logging.info("Starting compiller...")


class SmartError(Exception):
    """The error for Smart (syntaxe error)."""
    def __init__(self, message:str, nb_instruction:int=0):
        logging.critical("\033[31mError during build:")


        nbline, line_error = line_of_instruction(nb_instruction)

        print(f"~~~~~~~~~~\nAt {nbline} line:\n{line_error}\n~~~~~~~~~~\nError :\n{message}\n\033[0m")

        self.syntaxerror = message
        self.nbline = nbline

class SmartFunction:
    """Information about a smart function."""
    def __init__(self, name:str):
        """Set the attibute of the function."""
        self.name = name
        self.source_code_function = ""
        self.code_compile_f = ""
        self.function_adress = 0
        self.return_value = False

        self.called_function = False    # if False at the end of build, the function was never called

code_line = None

line_of_instruction = None

need_input = False

def split_code(
        code:str,
        sep:str | tuple[str, ...]=(" ",),
        string:tuple=("'", '"'),
        max_split:int=0
    ) -> list[str]:
    """Split a code, but ignore sep if it is in a str or char Smart Value.
    arg max for set the max split. If max=0, no limit of split."""

    if code == "":
        return ()
    
    on_str = False
    open_str = ""

    if isinstance(sep, str):
        sep = (sep,)

    split = []

    new_element = []

    nb_split = 0

    for char in code:
        if not on_str:
            if char in string:
                on_str = True
                open_str = char

            if char in sep:
                if max_split:
                    if nb_split == max_split:
                        new_element.append(char)
                        continue
                    else:
                        nb_split += 1
                split.append("".join(new_element))
                del new_element[:]

            else:
                new_element.append(char)
        
        else:
            if char == open_str:
                on_str = False
            
            new_element.append(char)
    
    if new_element != []:
        split.append("".join(new_element))
    
    return split


def compile_smarty(
        file:str="",
        argv:list | tuple=[],
        CODE_ADRESSE:int=0x400,
        make_file:bool=True,
        function_mode:tuple[
            bool,
            str,
            list[str],
            list[str],
            SmartFunction
        ]=(False, "", [], [], "", {}, None)
    ) -> None:
    """Start the compile from file."""
    global line_of_instruction, code_line

    class SmartBuiltIn:
        """Set the built in function of Smart.
        Warning: some function are not in this class because it is assembly function (print, goto...)"""
        
        input_code = "AD 11 D0 10 FB AD 10 D0 29 7F 60 "
        def smartInput() -> None:
            """Add an input function."""
            global need_input
            nonlocal code_compile, adress_conter
            need_input = True

            code_compile += "20 !  smart_input"     # set 2 space on placeholder for counting adress

            adress_conter += 3
        
        


    def line_of_instruction(nb_instruction:int) -> tuple[int, str]:
        """Return the number of line and the line of the instruction."""
        nb = 0
        line_counter = 0

        for line in code_line:

            nb += line.count(";")

            line_counter += 1

            if nb_instruction + 1 <= nb:
                return (line_counter + 1, code_line[line_counter-1])
        
        return (line_counter +1, code_line[line_counter-1])



    def get_char(char_type:str) -> str:
        """Return the char value of Smart."""
        if char_type[2] == "'":
            char = char_type[1]

            if char.islower():
                raise SmartError("char canno't be lower.", nb_instruction=line_conter)
            
            code_ascii = ord(char)

            code_hex = hex(code_ascii)[2:]
            code_hex = code_hex.upper()
            return code_hex

        else:
            raise SmartError("char value need 1 char.", line_conter)

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
            raise SmartError(f"Bad hex value '{code}'", line_conter)
    
    def set_one_A_value(value:str, one_addition:bool=False, recursiv_value:bool=False, forbiden_math:bool=False) -> str:
        """Return the value for set one A."""
        def control_math() -> None:
            """If forbiden_math is True, raise SmartError if there is a math in value."""
            if forbiden_math:
                raise SmartError(f"Math is forbiden for this value: '{value}'", line_conter)

        nonlocal adress_conter
        def eval_value() -> str:
            """Return asm value"""
            nonlocal adress_conter, code_compile
            if "+" in value:    # addition
                control_math()
                try:
                    value_1, value_2 = split_code(value, "+", max_split=1)
                
                    hex_value_2 = set_one_A_value(value_2, one_addition=True, recursiv_value=True)

                    if hex_value_2.startswith("6D "):
                        asm = f"{set_one_A_value(value_1, recursiv_value=True)}18 {hex_value_2}"

                    else:
                        asm = f"{set_one_A_value(value_1, recursiv_value=True)}18 69 {hex_value_2[3:]}"

                    return asm

                except SmartError as se:
                    raise SmartError(str(se), se.nbline)

                except:
                    raise SmartError(f"Error with math '+' : '{value}'", line_conter)

            elif value[0] == ".":
                variable = value[1:]

                if variable not in smart_var:
                    raise SmartError(f"Name error : name '{value}' is not defined.", line_conter)
                
                if not one_addition:
                    return f"AD {adress_for_RAM(smart_var[variable])} "
                else:
                    return f"6D {adress_for_RAM(smart_var[variable])} "
            

            elif value.startswith("0x"):
                hex_value = value[2:]

                control_hex(hex_value)


                return "A9 " + hex_value + " "
            
            
            elif value[0] in "0123456789":
                if len(value) > 3:
                    raise SmartError(f"Invalid value: {value}", line_conter)
                
                try:
                    value_int = int(value)
                except:
                    raise SmartError(f"Invalid int value: {value}")

                if value_int > 255:
                    raise SmartError(f"Invalid value: {value_int}, max int value is 255")
                
                value_int_to_hex = hex(value_int)[2:].upper()

                value_hex = ("0" if len(value_int_to_hex) == 1 else "") + value_int_to_hex

                return "A9 " + value_hex + " "

            elif value[0] == "'":
                return "A9 " + get_char(value) + " "
        
            elif value[0] == "\"":
                raise SmartError(f"Smart forbiden value: '{value}'", line_conter)

            elif ":" in value:  # call function for set on A

                func_name_value, func_arg_value = value.split(":", 1)

                if func_name_value == "input":
                    SmartBuiltIn.smartInput()
                    return ""
                
                else:

                    if func_name_value in function_name_usr:
                        """if not function_name_usr[func_name_value].return_value:
                            raise SmartError(f"Function '{func_name_value}' is not a return-function.", line_conter)"""

                    else:
                        raise SmartError(f"Function '{func_name_value}' not exist.", line_conter)

                    adress_conter += 13

                    text_code = f"!smart_call_func|{func_name_value}|{caller_ctx}|{adress_conter}"

                    function_replace.append(text_code)

                return text_code
        
            else:
                raise SmartError(f"Smart value error: {value}", line_conter)
        
        asm_v = eval_value()

        if not recursiv_value:
            adress_conter += asm_v.count(" ")

        return asm_v
    
    def good_asm(asm:str) -> bool:
        """Return True if assembly is good.
        Assembly is good if char is in A-F 0-9"""
        for char in asm:
            if char not in "ABCDEF0123456789":
                return False
        return True


    def adress_for_RAM(adress:int) -> str:
        """Return the RAM adress one hex.
        Exemple :
        768 -> 00 03"""
        adress_RAM = hex(adress)[2:]

        adress_RAM = "0" * (4 - len(adress_RAM)) + adress_RAM

        adress_RAM = adress_RAM[2:] + " " + adress_RAM[:2]
        return adress_RAM
    
    def good_variable_name(name:str) -> bool:
        """Return True if the name of variable is good, False else.
        An variable name can have :
        - Any letter lower (a-z). Special letter (éèëù...) are accepted.
        - Any number 0-9
        - underscore _"""
        for char in name:
            if (not (char.isalpha() or char.isdigit() or char == "_")) or char.isupper():
                return False
        return True

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    # -----------

    smart_var = {} if not function_mode[0] else function_mode[5]
    adress_var = 0x300 + len(smart_var)

    line_conter = 0

    adress_str = hex(CODE_ADRESSE)[2:].upper() + ": "

    code_compile = "0" * (6 - len(adress_str)) + adress_str if not function_mode[0] else ""

    go_to = {}

    function_name_usr: dict[str, SmartFunction] = function_mode[2] if function_mode[0] else {}

    go_to_replace = []
    function_replace = function_mode[3] if function_mode[0] else []

    adress_conter = 0

    CALLER_MAIN = "__MAIN__"
    caller_ctx = function_mode[4] if (function_mode[0] and len(function_mode) >= 5) else CALLER_MAIN

    if function_mode[0]:
        code_line = function_mode[1].split("\n")
        code_start = function_mode[1]
    else:
        sma = open(file, "r", encoding="UTF-8")

        code_start = sma.read()

        sma.close()

        code_line = code_start.split("\n")

    code = ""

    for line in code_line:
        line_tmp = line.split("//")[0] + "\n"
        #line_tmp = split_code(line, "//", max_split=1)[0] + "\n"
        code += line_tmp.lstrip(" ")
    

    #code = code.replace("\n", "").split(";")
    code = split_code(code.replace("\n", ""), ";")

    logging.info("Buiilding asm")

    jump_line = 0

    if code_start.replace(" ", "").replace("\n", "").replace("\t", "") == "":
        logging.warning("Smart file is empty!")

    for line in code:

        if jump_line:
            jump_line -= 1
            line_conter += 1
            continue

        if line == "" or line.replace(" ", "") == "":
            line_conter += 1
            logging.warning("Empty line detected.")
            continue


        if line[0] in ACUMULATOR_REGISTER:
            line = line.replace(" ", "")
            read_line = line.split("=", 1)
            

            r = read_line[0]

            if len(read_line) != 2:
                raise SmartError(f"Smart syntaxe error:\nline {line_conter}", line_conter)
        
            if r == "A":
                value_accumulator = set_one_A_value(read_line[1])
            else:
                value_accumulator = set_one_A_value(read_line[1], forbiden_math=True)
          
            code_compile += value_accumulator if r == "A" else "A2" + value_accumulator[2:] if r == "X" else "A0" + value_accumulator[2:]

            adress_conter -= 1 if r != "A" else 0
            
            logging.info("Build asm command: set on accumulator value")

        elif line[0] == "#":
            name = line[1:]

            if (" " in name or "\n" in name) or (name in ACUMULATOR_REGISTER):
                raise SmartError(f"Invalid name for goto : '{name}'", line_conter)

            hex_adress = hex(CODE_ADRESSE + adress_conter)[2:]

            
            hex_adress = "0" * (4-len(hex_adress)) + hex_adress


            go_to[name] = hex_adress

            logging.info("Build asm command: goto")

        
        elif line.startswith("."):      # variable
            
            line = line.replace(" ", "")[1:]

            var_name, value = line.split("=", 1)

            if not good_variable_name(var_name):
                raise SmartError(f"Bad variable name : '{var_name}'", line_conter)

            if var_name not in smart_var: # make new variable
                if len(smart_var) >= 256:
                    raise SmartError("Memory error : maximum variable are 256.", line_conter)
                smart_var[var_name] = adress_var
                adress_var += 1
            
            value_RAM = set_one_A_value(value)
                        
            code_compile += f"{value_RAM}8D {adress_for_RAM(smart_var[var_name])} "

            adress_conter += 3

            logging.info(f"Build asm command: using RAM for variable '{var_name}'")
        
        elif line.replace(" ", "").startswith("void"):      # make fonction
            if function_mode[0]:
                raise SmartError(f"Error with function: impossible to create new function on function.")

            func_name = line.split(" ")[1]

            if func_name[-1] != "{":
                raise SmartError("On function " + func_name + ", expected '{'", line_conter)

            func_name = func_name[:-1]

            if not good_variable_name(func_name):
                raise SmartError(f"Invalid name for {func_name}", line_conter)

            logging.debug(f"Building function '{func_name}'")

            
            # get the code of function:

            funciton_line = line_conter + 1

            func_code = ""

            number_open = 1

            try:
                while True:
                    code_line_func = code[funciton_line]
                    close_pos = None

                    for i, ch in enumerate(code_line_func):
                        if ch == "{":
                            number_open += 1
                        elif ch == "}":
                            number_open -= 1
                            if number_open == 0:
                                close_pos = i
                                break

                    if close_pos is not None:
                        inside = code_line_func[:close_pos]
                        if inside.replace(" ", "") != "":
                            func_code += inside + ";"

                        code[funciton_line] = code_line_func[close_pos + 1:]
                        break

                    func_code += code_line_func + ";"
                    funciton_line += 1
        


            except IndexError:
                raise SmartError("On function '" + func_name + "', brackets '{' was never closed.", line_conter)


            function_name_usr[func_name] = SmartFunction(func_name)
            function_name_usr[func_name].source_code_function = func_code

            jump_line = funciton_line - line_conter - 1

            

            logging.debug(f"'{func_name}' has been created.")
        
        elif line.replace(" ", "").startswith("return"):        # return value
            
            if not function_mode[0]:
                raise SmartError("Smart syntaxe error: 'return' key word can't be used outside function.", line_conter)
            
            try:
                value_return = line.strip().split(" ", 1)[1].replace(" ", "")
            except:
                raise SmartError(f"Smart syntaxe error: '{line}'", line_conter)

            code_compile += set_one_A_value(value_return)
            
            function_mode[6].return_value = True



        else:     # function
            if ":" not in line:
                raise SmartError("Smart invalid syntaxe", line_conter)

            line = line.replace(" ", "")

            function_name, function_arg = line.split(":", 1)
            #function_arg = function_arg.split(",")
            function_arg = split_code(function_arg, ",")

            if not good_variable_name(function_name):
                raise SmartError(f"Sintaxe error: '{function_name}'", line_conter)

            if function_name == "print":
                if len(function_arg) != 1:
                    raise SmartError("print function take 1 arg", line_conter)
                
                if function_arg[0] in ACUMULATOR_REGISTER:
                    if function_arg[0] != "A":
                        raise SmartError(f"print need 'A' registrer, not '{function_arg[0]}'", line_conter)
                    
                    code_compile += "20 EF FF "

                    adress_conter += 3
                

                elif function_arg[0][0] == "\"":
                    smart_str = function_arg[0]

                    if smart_str[-1] != "\"":
                        raise SmartError("str value was not closed.", line_conter)
                    
                    value_str = smart_str[1:-1]

                    if len(value_str) == 0:
                        logging.warning("str value is empty!")
                    elif len(value_str) == 1:
                        logging.warning("str value have a len of 1. Please use a char value.")

                    for char in value_str:
                        code_compile += set_one_A_value(f"'{char}'") + "20 EF FF "

                        adress_conter += 3
                
                else:
                    code_compile += set_one_A_value(function_arg[0])
                    code_compile += "20 EF FF "
                    adress_conter += 3
                
                logging.info("Build smart fonction as asm command: print")



            elif function_name == "quit":
                if function_arg != [""]:
                    raise SmartError("Function 'quit' not take arg.", line_conter)
                
                code_compile += "00 "

                logging.info("Build smart fonction as asm command: quit")
            
            elif function_name == "goto":
                if len(function_arg) != 1:
                    raise SmartError("Function 'goto' take 1 arg.", line_conter)
                
                name = function_arg[0]

                goto_tmp = f"!smart_tmp:goto|{name}"

                go_to_replace.append(goto_tmp)

                code_compile += "4C " + goto_tmp

                adress_conter += 3

                logging.info("Build smart fonction as asm command: goto")
            
            elif function_name == "asm_entry":
                if len(function_arg) != 1:
                    raise SmartError("Function asm_entry take 1 arg.", line_conter)
                
                asm = function_arg[0]

                if not (asm.startswith('"') and asm.endswith('"')):
                    raise SmartError(f"str value escepted, not '{asm}'")
                
                asm = asm[1:-1].strip(" ").replace(" ", "")

                if len(asm) == 0:
                    logging.warning(f"Empty assembly entry, at line {line_conter}")
                

                if ((len(asm) % 2) != 0) or (not good_asm(asm)):
                    raise SmartError(f"Invalid assembly entry, bad bytes was given.", line_conter)
                
                code_tmp = " ".join(asm[i:i+2] for i in range(0, len(asm), 2)) + " "

                code_compile += code_tmp

                adress_conter += code_tmp.count(" ")
            
            elif function_name == "input":
                logging.warning("'input' function is a return-function, but was used as a function.")

                SmartBuiltIn.smartInput()


            elif function_name in function_name_usr:

                # use a goto

                adress_conter += 13

                text_code = f"!smart_call_func|{function_name}|{caller_ctx}|{adress_conter}"

                function_replace.append(text_code)

                code_compile += text_code

            
            else:
                raise SmartError(f"Function '{function_name}' not exist.", line_conter)

        line_conter += 1
    
    if not function_mode[0]:
        code_compile += "00 "
    else:
        code_compile += "4C 00 00 "
    
    if need_input and not function_mode[0]:
        input_adress = adress_conter + CODE_ADRESSE + 1

        hex_input_adress = hex(input_adress)[2:].upper()
        hex_input_adress = "0" * (4 - len(hex_input_adress)) + hex_input_adress

        code_compile += SmartBuiltIn.input_code
        adress_conter += SmartBuiltIn.input_code.count(" ")

        code_compile = code_compile.replace("!  smart_input", f"{hex_input_adress[2:]} {hex_input_adress[:2]} ")

    # compile function:

    if not function_mode[0]:
        for function in function_name_usr:

            code = function_name_usr[function].source_code_function

            smart_func = function_name_usr[function]

            function_name_usr[function].code_compile_f = compile_smarty(make_file=False, function_mode=(True, code, function_name_usr, function_replace, function, smart_var, smart_func), CODE_ADRESSE=CODE_ADRESSE + adress_conter + 1)



        # set the function:

        for f in function_name_usr:

            function_name_usr[f].function_adress = adress_conter

            code_func = function_name_usr[f].code_compile_f
            
            code_compile += code_func

            adress_conter += code_func.count(" ") + 13 * code_func.count("!smart_call_func|")

        # call function
        for i in range(2):
            for f in function_replace:
                function = f

                parts = function.split("|")
                if len(parts) == 3:
                    function_name_tmp = parts[1]
                    caller_ctx_tmp = CALLER_MAIN
                    r_offset = int(parts[2])
                else:
                    function_name_tmp = parts[1]
                    caller_ctx_tmp = parts[2]
                    r_offset = int(parts[3])

                adress_func = CODE_ADRESSE + function_name_usr[function_name_tmp].function_adress + 1

                hex_adress_function = hex(adress_func)[2:].upper()
                hex_adress_function = "0" * (4 - len(hex_adress_function)) + hex_adress_function
                hex_adress_function = f"{hex_adress_function[2:]} {hex_adress_function[:2]}"

                func_len = function_name_usr[function_name_tmp].code_compile_f.count(" ") + 13 * function_name_usr[function_name_tmp].code_compile_f.count("!smart_call_func|")

                return_aress = hex(adress_func + func_len - 1)[2:].upper()
                return_aress = "0" * (4 - len(return_aress)) + return_aress

                return_aress_2 = hex(adress_func + func_len - 2)[2:].upper()
                return_aress_2 = "0" * (4 - len(return_aress_2)) + return_aress_2

                caller_base = CODE_ADRESSE if caller_ctx_tmp == CALLER_MAIN else CODE_ADRESSE + function_name_usr[caller_ctx_tmp].function_adress + 1
                r_adress = hex(caller_base + r_offset)[2:].upper()
                r_adress = "0" * (4 - len(r_adress)) + r_adress

                code_compile = code_compile.replace(function, f"A9 {r_adress[:2]} 8D {return_aress[2:]} {return_aress[:2]} A9 {r_adress[2:]} 8D {return_aress_2[2:]} {return_aress_2[:2]} 4C {hex_adress_function} ")

                function_name_usr[function_name_tmp].called_function = True

    if not function_mode[0]:
        for name, f in function_name_usr.items():
            if not f.called_function:
                logging.warning(f"Function '{name}' was never called.")

    # set the goto:

    for goto in go_to_replace:
        goto_name = goto.split("|")[1]

        try:
            adress = go_to[goto_name]
                
        except KeyError:
            raise SmartError(f"'{name}' is not defined for goto !", line_conter)

        code_compile = code_compile.replace(goto, f"{adress[2:]} {adress[:2]} ")
    


    if not function_mode[0]:

        logging.info("Build completed!")
        
        if make_file:
            print(f"\n\n{code_compile}\n\n")
            
            Path(os.path.splitext(argv[1])[0] + ".asm").write_text(code_compile, encoding="UTF-8")

            logging.info(f"asm file saved as {os.path.splitext(argv[1])[0]}.asm")
        
        logging.info("Build end.")

        logging.info(f"Memory info: virtual smart memory: 256bytes, used by programme: {len(smart_var)}bytes, using {len(smart_var) / 256 * 100}% of smart virtual memory. Programme size: used {adress_conter} bytes from {hex(CODE_ADRESSE)}")


    return code_compile