# -*- coding: utf-8 -*-

"""
The compiller for smart.

Fonction: compile_smarty for start the compile of a smart code.
"""

from pathlib import Path
import os
import logging

from compiller_tool.string_tool import split_code, replace_code, in_code
from compiller_tool.color_tool import ColoredFormatter
from compiller_tool import import_tool

logging.basicConfig(format="SmartCompiller %(levelname)s: %(message)s", level=logging.INFO)

for handler in logging.root.handlers:
    handler.setFormatter(ColoredFormatter('SmartCompiller %(levelname)s: %(message)s'))




ESCAPE_CHAR = {"\\r":"\r", "\\\"":"\""}        # the escape characters for str and char (\r...)

class CompileError(Exception):
    """An error with compile (file not found, unknow error...).
    Use SmartError for error with code (syntaxe, bad value...)"""
    def __init__(self, message:str="Error"):
        logging.critical(message)

        self.error = message

class SmartError(CompileError):
    """The error for Smart (syntaxe error)."""
    def __init__(self, message:str, nb_instruction:int=0):
        logging.critical(ColoredFormatter.COLORS["CRITICAL"] + "Error during build:")


        nbline, line_error = line_of_instruction(nb_instruction)

        if warning_endline[0]:
            text_endline = ColoredFormatter.COLORS["WARNING"] + f"Maybe you forget ';' at {warning_endline[1]} line?"
        else:
            text_endline = ""

        print(f"~~~~~~~~~~\nAt {nbline} line:\n{line_error}\n~~~~~~~~~~\nError :\n{message}\n{text_endline}\n{ColoredFormatter.RESET}")

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

warning_endline = (False, )     # if an line not end by ; } or // in line or the last line

def get_bloc(line_conter:int, code:str, error_message:str="") -> str:
    """Return the content of bloc {}
    
    error_message is the text for info about error."""
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
        raise SmartError(error_message + ", brackets '{' was never closed.", line_conter)
    
    return func_code, funciton_line



def compile_smarty(
        file:str="",
        argv:list | tuple=[],
        CODE_ADRESSE:int=0x400,
        make_file:bool=True,
        function_mode:dict[
            str,
            bool | str | list | dict | SmartFunction | None
        ]={"function_mode":False, "source_code":"", "global_function":[], "global_function_replace":[], "function_caller_ctx":"", "global_var":{}, "smart_func":None, "if_mode":False, "global_goto":{}, "goto_replace":[]},
        bin_outpout_file:bool=False,
        module_mode:bool=False
    ) -> None:
    """Start the compile from file."""
    global line_of_instruction, code_line, warning_endline
    logging.info("Starting compiller...")
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

    def get_str(string:str) -> str:
        """Return the str value. Add the escape char."""

        string = string.strip()

        if not string.startswith('"'):  # error if function was called in other value to str
            raise SmartError(f"Value '{string}' is not a str value.", line_conter)
        

        str_value = ""
        escape_char = False
        end = False

        for char in string[1:]:
            if end: # a char is after the " for close
                raise SmartError(f"Invalid syntaxe after str value: '{string}'", line_conter)
            
            if char == '"' and not escape_char:
                end = True
                continue
                
            str_value += char

            if char == "\\":
                escape_char = True
            
            else:
                escape_char = False

        # replace char:
        for char in ESCAPE_CHAR:
            replace = ESCAPE_CHAR[char]

            str_value = str_value.replace(char, replace)


        if len(str_value) == 0:
            logging.warning("str value is empty!")
        elif len(str_value) == 1:
            logging.warning("str value have a len of 1. Please use a char value.")

        return str_value


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
    
    def set_one_A_value(value:str, one_math:bool=False, hex_math_op:str="", recursiv_value:bool=False, forbiden_math:bool=False) -> str:
        """Return the value for set one A."""
        def imediate_value(value:str) -> bool:
            """Return True if the value is an imediate value else false.
            A9 41 : imediate value (LDA #41)
            AD 00 04 : adress value (LDA $0400)
            """
            try:
                start = value.replace(" ", "")[0:2]
            except IndexError:
                return False
            

            if start in ("A9", "69", "E9"):
                return True
            return False

        def control_math() -> None:
            """If forbiden_math is True, raise SmartError if there is a math in value."""
            if forbiden_math:
                raise SmartError(f"Math is forbiden for this value: '{value}'", line_conter)
        global counter_adress_value
        nonlocal adress_conter

        def eval_value() -> str:
            """Return asm value"""
            global counter_adress_value
            nonlocal adress_conter, code_compile
            if in_code("+", value):    # addition
                control_math()
                try:
                    value_1, value_2 = split_code(value, "+", max_split=1)

                    hex_value_1 = set_one_A_value(value_1, recursiv_value=True)

                    counter_adress_value += 1       # add for the OP code 18
                
                    hex_value_2 = set_one_A_value(value_2, one_math=True, recursiv_value=True, hex_math_op="69")

                    if not imediate_value(hex_value_2):     # adress value
                        asm = f"{hex_value_1}18 6D {hex_value_2[3:]}"


                    else:
                        asm = f"{hex_value_1}18 69 {hex_value_2[3:]}"       #valeur imédiate
                        
                    return asm

                except SmartError as se:
                    raise SmartError(str(se), se.nbline)

                except:
                    raise SmartError(f"Error with math '+' : '{value}'", line_conter)
            
            elif in_code("-", value):    # substraction
                control_math()
                try:
                    value_1, value_2 = split_code(value, "-", max_split=1)

                    hex_value_1 = set_one_A_value(value_1, recursiv_value=True)

                    counter_adress_value += 1       # add for the OP code 18
                
                    hex_value_2 = set_one_A_value(value_2, one_math=True, recursiv_value=True, hex_math_op="E9")

                    if not imediate_value(hex_value_2):
                        asm = f"{hex_value_1}38 ED {hex_value_2[3:]}"       # adress value
                        
                    else:
                        asm = f"{hex_value_1}38 E9 {hex_value_2[3:]}"      # valeur immédiate
                        
                        

                    return asm

                except SmartError as se:
                    raise SmartError(str(se), se.nbline)

                except:
                    raise SmartError(f"Error with math '-' : '{value}'", line_conter)
                
            elif in_code("==", value):
                try:
                    value_1, value_2 = split_code(value, "==", max_split=1)

                    hex_value_1 = set_one_A_value(value_1, one_math=True, recursiv_value=True)#a terminer

                    hex_value_2 = set_one_A_value(value_2, one_math=True, recursiv_value=True)

                    if not imediate_value(hex_value_2):
                        
                        asm = f"{hex_value_1}CD {hex_value_2[3:]}"      # adress value

                    else:
                        asm = f"{hex_value_1}C9 {hex_value_2[3:]}"      # imediate value
                        counter_adress_value -= 1

                    asm += "D0 04 A9 01 D0 02 A9 00 "

                    counter_adress_value += 9
                    
                    return asm


                except SmartError as se:
                    raise SmartError(str(se), se.nbline)

            elif value[0] == ".":
                variable = value[1:]

                if variable not in smart_var:
                    raise SmartError(f"Name error : name '{value}' is not defined.", line_conter)
                
                counter_adress_value += 3
                
                if not one_math:
                    return f"AD {adress_for_RAM(smart_var[variable])} "
                else:
                    return f"AD {adress_for_RAM(smart_var[variable])} " # hex_math_op before AD ?
            
            elif value.startswith("True"):
                counter_adress_value += 2
                return "A9 01 "

            elif value.startswith("False"):
                counter_adress_value += 2
                return "A9 00 "

            elif value.startswith("0x"):
                hex_value = value[2:]

                control_hex(hex_value)

                counter_adress_value += 2


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

                counter_adress_value += 2

                load = "A9 " if not one_math else hex_math_op + " "

                return load + value_hex + " "

            elif value[0] == "'":
                counter_adress_value += 2
                return "A9 " + get_char(value) + " "
        
            elif value[0] == "\"":
                raise SmartError(f"Smart forbiden value: '{value}'", line_conter)

            elif in_code(":", value):

                # save A to 0x02E7 if the function is a return-function
                saver_A = "8D E7 02 "

                counter_adress_value += 3

                func_name_value, func_arg_value = value.split(":", 1)

                if func_name_value == "input":
                    SmartBuiltIn.smartInput()
                    counter_adress_value += 3
                    return ""
                
                else:

                    if func_name_value in function_name_usr:
                        """if not function_name_usr[func_name_value].return_value:
                            raise SmartError(f"Function '{func_name_value}' is not a return-function.", line_conter)"""

                    else:
                        raise SmartError(f"Function '{func_name_value}' not exist.", line_conter)

                    adress_conter += 13

                    text_code = f"!smart_call_func|{func_name_value}|{caller_ctx}|{adress_conter + counter_adress_value}"

                    
                    function_replace.append(text_code)

                    counter_adress_value += 3

                    if not one_math:
                        return saver_A + text_code + "AD E8 02 "
                    else:
                        return saver_A + text_code + f"{hex_math_op} E8 02 "
      
            else:
                raise SmartError(f"Smart value error: {value}", line_conter)
        
        if not recursiv_value:
            counter_adress_value = 0

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
    
    import_tool.config_import(compile_smarty)

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    # -----------

    smart_var = {} if not function_mode["function_mode"] else function_mode["global_var"]
    adress_var = 0x300 + len(smart_var)

    line_conter = 0

    adress_str = hex(CODE_ADRESSE)[2:].upper() + ": "

    code_compile = "0" * (6 - len(adress_str)) + adress_str if not function_mode["function_mode"] else ""

    go_to = {} if not function_mode["if_mode"] else function_mode["global_goto"]

    if function_mode["function_mode"]:
        return_line = False     # became True when they are the return line (if an line is after return line, raise SmartError)

    function_name_usr: dict[str, SmartFunction] = function_mode["global_function"] if function_mode["function_mode"] else {}

    go_to_replace = [] if not function_mode["if_mode"] else function_mode["goto_replace"]
    function_replace = function_mode["global_function_replace"] if function_mode["function_mode"] else []

    adress_conter = 0

    CALLER_MAIN = "__MAIN__"
    caller_ctx = function_mode["function_caller_ctx"] if (function_mode["function_mode"] and len(function_mode) >= 5) else CALLER_MAIN

    if function_mode["function_mode"]:
        code_line = function_mode["source_code"].split("\n")
        code_start = function_mode["source_code"]
    else:
        try:
            sma = open(file, "r", encoding="UTF-8")

            code_start = sma.read()

            sma.close()

            code_line = code_start.split("\n")
        except FileNotFoundError:
            raise CompileError(f"File not found: '{file}'")

    #control syntaxe warning:
    for i, line in enumerate(code_line):
        line_controle = line.replace(" ", "").replace("\t", "")

        if line_controle:
            line_controle = split_code(line_controle, "//")[0]

        if not(line_controle == "" or line_controle.endswith(";") or line_controle.endswith("}")):
            i += 1
            warning_endline = (True, i)

            logging.warning(f"Sintaxe warn: at line {i}, can't identify end. Maybe you have forget ';'?")
            break

    code = ""

    for line in code_line:
        line_tmp = line.split("//")[0].strip() + "\n"
        code += line_tmp
    
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

        if function_mode["function_mode"]:
            if return_line:
                raise SmartError("On function {}, value was return before the end of function.".format(function_mode["smart_func"].name))


        if line[0] in ACUMULATOR_REGISTER:
            line = replace_code(line, " ", "")
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

            hex_adress = hex(CODE_ADRESSE + adress_conter)[2:].upper()

            
            hex_adress = "0" * (4-len(hex_adress)) + hex_adress


            go_to[name] = hex_adress

            logging.info("Build asm command: goto")

        
        elif line.startswith("."):      # variable
            
            line = replace_code(line, " ", "")[1:]

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

        elif line.lstrip().startswith("if"):
            line_2 = replace_code(line, " ", "")[2:]

            if not line_2.endswith("{"):
                raise SmartError("On if bloc, expected '{'", line_conter)
            else:
                line_2 = line_2[:-1]

            code_compile += set_one_A_value(line_2)

            bloc_code, bloc_line = get_bloc(line_conter, code, error_message="On if bloc")

            jump_line = bloc_line - line_conter - 1
            
            code_compile += "C9 00 D0 03 4C {} "
            adress_conter += 7

            code_if = compile_smarty(
                make_file=False,
                function_mode={"function_mode":True, "source_code":bloc_code, "global_function":function_name_usr, "global_function_replace":function_replace, "function_caller_ctx":caller_ctx, "global_var":smart_var, "smart_func":None, "if_mode":True, "global_goto":go_to, "goto_replace":go_to_replace},
                CODE_ADRESSE=CODE_ADRESSE + adress_conter
            )

            new_adress = code_if.count(" ") + code_if.count("!smart_call_func|") * 13 + code_if.count("!smart_tmp:goto|") * 3 - code_if.count("!smart_tmp:goto|")

            hex_adress_if = hex(CODE_ADRESSE + adress_conter + new_adress)[2:].upper()
            hex_adress_if = "0" * (4 - len(hex_adress_if)) + hex_adress_if
            hex_adress_if = hex_adress_if[2:] + " " + hex_adress_if[:2]


            code_compile = code_compile.format(hex_adress_if)

            adress_conter += new_adress
            code_compile += code_if


        
        elif line.lstrip().startswith("void"):      # make fonction
            if function_mode["function_mode"]:
                raise SmartError(f"Error with function: impossible to create new function on function.", line_conter)

            func_name = line.split(" ")[1]

            if func_name[-1] != "{":
                raise SmartError("On function " + func_name + ", expected '{'", line_conter)

            func_name = func_name[:-1]

            if not good_variable_name(func_name):
                raise SmartError(f"Invalid name for {func_name}", line_conter)

            logging.debug(f"Building function '{func_name}'")
           
            func_code, funciton_line = get_bloc(line_conter, code, error_message="On function '" + func_name + "'")

            function_name_usr[func_name] = SmartFunction(func_name)
            function_name_usr[func_name].source_code_function = func_code

            jump_line = funciton_line - line_conter - 1

            logging.debug(f"'{func_name}' has been created.")
        
        elif line.lstrip().startswith("return "):        # return value
            
            if not(function_mode["function_mode"]) or function_mode["if_mode"]:
                raise SmartError("Smart syntaxe error: 'return' key word can't be used outside function.", line_conter)
            
            try:
                value_return = replace_code(line.strip().split(" ", 1)[1], " ", "")
            except:
                raise SmartError(f"Smart syntaxe error: '{line}'", line_conter)


            code_compile += set_one_A_value(value_return)
            
            function_mode["smart_func"].return_value = True

            # save new A at RAM
            code_compile += "8D E8 02 "
            adress_conter += 3

            # reuse the old value for A
            code_compile += "AD E7 02 "
            adress_conter += 3

            return_line = True

        elif line.lstrip().startswith("import "):
            line_import = split_code(line, " ")[1:]

            try:

                if len(line_import) == 1:   # search in all directory
                    if not(line_import[0].startswith('"') and line_import[0].endswith('"')):
                        raise SmartError("Need a str value for path, in import.")
                    name_import = line_import[0][1:-1]
                    import_info = import_tool.import_all(name_import, CODE_ADRESSE + adress_conter)


                elif len(line_import) == 3: # search in a spesific directory (smart, lib or path of code)
                    line_from = split_code("".join(line_import), "from")

                    if len(line_from) != 2:
                        raise SmartError("Sintaxe error: excepted 'from'.", line_conter)

                    name_import, type_import = line_from

                    if not(name_import.startswith('"') and name_import.endswith('"')):
                        raise SmartError("Need a str value for path, in import.")
                    else:
                        name_import = name_import[1:-1]
                    
                    
                        if type_import == '"file"':
                            import_info = import_tool.import_module(name_import, CODE_ADRESSE + adress_conter)

                        elif type_import == '"lib"':
                            import_info = import_tool.import_lib(name_import, CODE_ADRESSE + adress_conter)

                        elif type_import == '"smart"':
                            import_info = import_tool.import_smart(name_import, CODE_ADRESSE + adress_conter)
                        
                        else:
                            raise SmartError('Unknow import type. Must be "file", "lib", "smart"')
                    
            except SmartError as se:
                raise SmartError("Error on module '{}':\n\t{}".format(name_import, (str(se)[1:-1].replace(",", "\n\t"))))
            except import_tool.ModuleError as me:
                raise SmartError("Error during importing module:\n" + str(me))
                
            adress_delta = import_info.binary.count(" ")

            code_compile += import_info.binary
            adress_conter += adress_delta

            function_name_usr |= import_info.function
            smart_var |= import_info.variables


            adress_conter += 2

            new_adress_module = adress_for_RAM(CODE_ADRESSE + adress_conter) + " "

            code_compile = code_compile.replace("!smart_module_goto", new_adress_module)
            
            

        else:     # function
            if not in_code(":", line):
                raise SmartError("Smart invalid syntaxe", line_conter)

            line = replace_code(line, " ", "")

            function_name, function_arg = line.split(":", 1)

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

                    """if smart_str[-1] != "\"":
                        raise SmartError("str value was not closed.", line_conter)
                    
                    value_str = smart_str[1:-1]"""

                    value_str = get_str(smart_str)



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

                asm_str = get_str(asm).strip(" ").replace(" ", "")

                if len(asm_str) == 0:
                    logging.warning(f"Empty assembly entry, at line {line_conter}")
                

                if ((len(asm_str) % 2) != 0) or (not good_asm(asm_str)):
                    raise SmartError(f"Invalid assembly entry, bad bytes was given.", line_conter)
                
                code_tmp = " ".join(asm_str[i:i+2] for i in range(0, len(asm_str), 2)) + " "

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
        
    if function_mode["if_mode"]:
        pass
    
    elif module_mode:
        code_compile += "4C !smart_module_goto"

    elif function_mode["function_mode"]:
        code_compile += "4C 00 00 "
    
    else:
        code_compile += "00 "
    
    if need_input and not function_mode["function_mode"]:
        input_adress = adress_conter + CODE_ADRESSE + 1

        hex_input_adress = hex(input_adress)[2:].upper()
        hex_input_adress = "0" * (4 - len(hex_input_adress)) + hex_input_adress

        code_compile += SmartBuiltIn.input_code
        adress_conter += SmartBuiltIn.input_code.count(" ")

        code_compile = code_compile.replace("!  smart_input", f"{hex_input_adress[2:]} {hex_input_adress[:2]} ")

    # compile function:

    if not function_mode["function_mode"]:
        for function in function_name_usr:

            code = function_name_usr[function].source_code_function

            smart_func = function_name_usr[function]

            function_name_usr[function].code_compile_f = compile_smarty(
                make_file=False,
                function_mode={"function_mode":True, "source_code":code, "global_function":function_name_usr, "global_function_replace":function_replace, "function_caller_ctx":function, "global_var":smart_var, "smart_func":smart_func, "if_mode":False},
                CODE_ADRESSE=CODE_ADRESSE + adress_conter + 1
            )



        # set the function:

        for f in function_name_usr:

            function_name_usr[f].function_adress = adress_conter

            code_func = function_name_usr[f].code_compile_f
            
            code_compile += code_func

            adress_conter += code_func.count(" ") + 13 * code_func.count("!smart_call_func|")

        # call function
        for i in range(2):
            for function in function_replace:

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

    if not function_mode["function_mode"]:
        for name, f in function_name_usr.items():
            if not f.called_function:
                logging.warning(f"Function '{name}' was never called.")

    # set the goto:

    if not function_mode["if_mode"]:
        for goto in go_to_replace:
            goto_name = goto.split("|")[1]

            try:
                adress = go_to[goto_name]
                    
            except KeyError:
                raise SmartError(f"'{name}' is not defined for goto !", line_conter)

            code_compile = code_compile.replace(goto, f"{adress[2:]} {adress[:2]} ")
        


    if not function_mode["function_mode"]:
        if bin_outpout_file:
            code_bin = "".join(chr(int(byte, base=16)) for byte in code_compile.split(" ")[1:-1])   # code_bin can have error with UTF-8, used for print only
            
            hex_bytes = [b for b in code_compile.split(" ")[1:-1] if b]     # used for file
            data = bytes(int(b, 16) for b in hex_bytes)
            
        else:
            code_bin = code_compile

        logging.info("Build completed!")
        
        if make_file:
            print(f"\n\n{code_bin}\n\n")
            
            if bin_outpout_file:
                Path(os.path.splitext(argv[1])[0] + ".bin").write_bytes(data)
                logging.info(f"bin file saved as {os.path.splitext(argv[1])[0]}.bin")

            else:
                Path(os.path.splitext(argv[1])[0] + ".hex").write_text(code_bin, encoding="UTF-8")

                logging.info(f"hex file saved as {os.path.splitext(argv[1])[0]}.hex")
        
        logging.info("Build end.")

        logging.info(f"Memory info: virtual smart memory: 256bytes, used by programme: {len(smart_var)}bytes, using {len(smart_var) / 256 * 100}% of smart virtual memory. Programme size: used {adress_conter} bytes from {hex(CODE_ADRESSE)}")

    if module_mode:
        return import_tool.ModuleInfo(code_compile, smart_var, function_name_usr)

    else:

        return code_compile