# -*- coding: utf-8 -*-

"""
The compiller for smart.

Fonction: compile_smarty for start the compile of a smart code.
"""

from pathlib import Path
import os
import logging
import re

from compiller_tool.string_tool import split_code, replace_code, in_code, good_variable_name, get_char_from_str, EscapeChar
from compiller_tool.color_tool import ColoredFormatter
from compiller_tool.smart_exception import CompileError, SmartError, config_exception, confirm_user
from compiller_tool import compiller_data_run
from compiller_tool import import_tool
from compiller_tool import smart_obj

logging.basicConfig(
    format="SmartCompiller %(levelname)s: %(message)s",
    level=logging.INFO
)

for handler in logging.root.handlers:
    handler.setFormatter(ColoredFormatter('SmartCompiller %(levelname)s: %(message)s'))
    handler.terminator = ''  # Supprime le newline automatique pour permettre input() sur la même ligne

FUNCTION_PATTERN = "^[a-z_][a-z0-9_]*.*:"



code_line = None

line_of_instruction = None

need_input = False



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
            bool | str | list | dict | smart_obj.SmartFunction | None
        ]={"function_mode":False, "source_code":"", "global_function":[], "global_function_replace":[], "function_caller_ctx":"", "global_var":{}, "smart_func":None, "if_mode":False, "global_goto":{}, "goto_replace":[], "while_mode":False},
        bin_outpout_file:bool=False,
        module_name:str="*" # module name is '*' if main module.
    ) -> None:
    """Start the compile from file."""
    global line_of_instruction, code_line#, warning_endline
    logging.info("Starting compiller...")

    module_mode = module_name != "*"
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
        
        BUILT_IN_NAME_RETURN = ["input"]
        BUILT_IN_NAME_NORETURN = ["print", "quit", "goto", "asm_entry"]

        BUILT_IN_NAME = BUILT_IN_NAME_RETURN + BUILT_IN_NAME_NORETURN


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

    config_exception(line_of_instruction)

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
                escape_char = not escape_char
            
            else:
                escape_char = False

        # replace char:

        str_value = str_value.replace(EscapeChar.DOUBLE_SLASH, EscapeChar.PLACE_HOLDER_SLASH)   # use a placeholder for double slash

        for char in EscapeChar.ESCAPE_CHAR:
            replace = EscapeChar.ESCAPE_CHAR[char]

            str_value = str_value.replace(char, replace)
        
        str_value = str_value.replace(EscapeChar.PLACE_HOLDER_SLASH, "\\")


        if len(str_value) == 0:
            logging.warning("str value is empty!")
        elif len(str_value) == 1:
            logging.warning("str value have a len of 1. Please use a char value.")

        return str_value


    def get_char(char_type:str) -> str:
        """Return the char value of Smart."""
        def char_error() -> None:
            """Raise SmartError for error if the char value don't have 1 character."""
            raise SmartError(f"The char value `{char_type}` don't have 1 character.")

        if char_type.startswith("'") and char_type.endswith("'"):
            char = char_type[1:-1]

            if len(char) == 2 and char.startswith("\\"):
                if char in EscapeChar.ESCAPE_CHAR:
                    code_ascii = ord(EscapeChar.ESCAPE_CHAR[char])
                else:
                    char_error()

            elif len(char) == 1:
                if char.islower():
                    raise SmartError("char canno't be lower.", line_conter)
                
                if char == "'":
                    raise SmartError(f"Error with char value `{char_type}`.")
                
                code_ascii = ord(char)

            else:
                char_error()
            
            code_hex = hex(code_ascii)[2:]
            code_hex = code_hex.upper()
            return code_hex

        else:
            raise SmartError(f"The char value (`{char_type}`) was never closed.", line_conter)

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
    
    def set_one_A_value(value:str, one_math:bool=False, recursiv_value:bool=False, forbiden_math:bool=False) -> str:
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
            
            if start == "A9":
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

            if in_code("*", value):
                control_math()
                try:
                    value_1, value_2 = split_code(value, "*", max_split=1)

                    asm = ""

                    hex_value_1 = set_one_A_value(value_1, recursiv_value=True)

                    asm += hex_value_1 + "8D F0 02 A9 00 "  # save value 1 on ram and set A to 00.
                    counter_adress_value += 5

                    value_2_tmp = set_one_A_value(value_2, one_math=True, recursiv_value=True)
                
                    hex_value_2 = "A2" + value_2_tmp[2:] if value_2_tmp.startswith("A9") else "AE" + value_2_tmp[2:]

                    asm += hex_value_2

                    asm += "CA "    # decrement X
                    counter_adress_value += 1

                    asm += "18 6D F0 02 "   # add to A hex_value_2
                    asm += "E0 00 D0 F7 "   # continue or not the loop

                    counter_adress_value += 8

                    return asm

                except SmartError as se:
                    raise SmartError(str(se), se.nbline)

                except:
                    raise SmartError(f"Error with math '*' : '{value}'", line_conter)
            
            elif in_code("/", value):
                control_math()
                try:
                    value_1, value_2 = split_code(value, "/", max_split=1)

                    asm = ""

                    hex_value_2 = set_one_A_value(value_2, recursiv_value=True)

                    asm += hex_value_2 + "8D F0 02 "  # save value 2 on ram
                    counter_adress_value += 3

                    if hex_value_2 == "A9 00 ":       # division by 0
                        confirm_user(f"Division by 0: {value}. It make an infinit loop! Continue compilation ? ", line_counter=line_conter)

                    hex_value_1 = set_one_A_value(value_1, one_math=True, recursiv_value=True)
                    
                    asm += hex_value_1

                    asm += "CD F0 02 " 
                    asm += "90 0A "    
                    counter_adress_value += 5

                    asm += "A2 00 E8 "    # set X to 00, and increment X on loop.
                    counter_adress_value += 3

                    asm += "38 ED F0 02 "      # substract to A hex_value_2
                    asm += "CD F0 02 B0 F6 "   # continue or not the loop

                    counter_adress_value += 9

                    asm += "8A "
                    counter_adress_value += 1

                    return asm

                except SmartError as se:
                    raise SmartError(str(se), se.nbline)

                except:
                    raise SmartError(f"Error with math '/' : '{value}'", line_conter)
            


            elif in_code("+", value):    # addition
                control_math()
                try:
                    value_1, value_2 = split_code(value, "+", max_split=1)

                    hex_value_1 = set_one_A_value(value_1, recursiv_value=True)

                    counter_adress_value += 1       # add for the OP code 18
                
                    hex_value_2 = set_one_A_value(value_2, one_math=True, recursiv_value=True)

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
                
                    hex_value_2 = set_one_A_value(value_2, one_math=True, recursiv_value=True)

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

                    hex_value_1 = set_one_A_value(value_1, one_math=True, recursiv_value=True)

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
                

                return f"AD {adress_for_RAM(smart_var[variable].ram_adress)} "

            
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

                return "A9 " + value_hex + " "

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

                if func_name_value in SmartBuiltIn.BUILT_IN_NAME_RETURN:
                    if func_name_value == "input":
                        SmartBuiltIn.smartInput()
                        counter_adress_value += 3
                        return ""
                
                elif func_name_value in SmartBuiltIn.BUILT_IN_NAME_NORETURN:
                    raise SmartError(f"Built in function {func_name_value} is not a return-function.")

                else:

                    if func_name_value in function_name_usr:
                        if not function_name_usr[func_name_value].return_value:
                            raise SmartError(f"Function '{func_name_value}' is not a return-function.", line_conter)

                    else:
                        raise SmartError(f"Function '{func_name_value}' not exist.", line_conter)

                    adress_conter += 13

                    text_code = f"!smart_call_func|{func_name_value}|{caller_ctx}|{adress_conter + counter_adress_value}"

                    
                    function_replace.append(text_code)

                    counter_adress_value += 3

                    return saver_A + text_code + "AD E8 02 "

      
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
            
    
    import_tool.config_import(compile_smarty)

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    # -----------

    on_loop = False

    if "while_mode" in function_mode:
        if function_mode["while_mode"]:
            on_loop = True


    last_if = False     # True if the last operation is if on Smart (for else).

    smart_var:dict[str, smart_obj.SmartVariable] = {} if not function_mode["function_mode"] else function_mode["global_var"]
    adress_var = 0x300 + len(smart_var)

    line_conter = 0

    adress_str = hex(CODE_ADRESSE)[2:].upper() + ": "

    code_compile = "0" * (6 - len(adress_str)) + adress_str if not function_mode["function_mode"] else ""

    go_to:dict[str, smart_obj.SmartGoto] = {} if not function_mode["if_mode"] else function_mode["global_goto"]

    if function_mode["function_mode"]:
        return_line = False     # became True when they are the return line (if an line is after return line, raise SmartError)

    function_name_usr: dict[str, smart_obj.SmartFunction] = function_mode["global_function"] if function_mode["function_mode"] else {}

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
            compiller_data_run.warning_endline = (True, i, module_name)

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


            go_to[name] = smart_obj.SmartGoto(name, hex_adress)

            logging.info("Build asm command: goto")

        
        elif line.startswith("."):      # variable
            
            line = replace_code(line, " ", "")[1:]

            var_name, value = line.split("=", 1)

            if not good_variable_name(var_name):
                raise SmartError(f"Bad variable name : '{var_name}'", line_conter)

            if var_name not in smart_var: # make new variable
                if len(smart_var) >= 256:
                    raise SmartError("Memory error : maximum variable are 256.", line_conter)
                smart_var[var_name] = smart_obj.SmartVariable(var_name, adress_var)
                adress_var += 1
            
            value_RAM = set_one_A_value(value)
                        
            code_compile += f"{value_RAM}8D {adress_for_RAM(smart_var[var_name].ram_adress)} "

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
            
            code_compile += "C9 00 D0 08 A9 01 8D E9 02 4C {} A9 00 8D E9 02 "
            adress_conter += 17

            code_if = compile_smarty(
                make_file=False,
                function_mode={"function_mode":True, "source_code":bloc_code, "global_function":function_name_usr, "global_function_replace":function_replace, "function_caller_ctx":caller_ctx, "global_var":smart_var, "smart_func":None, "if_mode":True, "global_goto":go_to, "goto_replace":go_to_replace, "while_mode":function_mode["while_mode"] if "while_mode" in function_mode else False},
                CODE_ADRESSE=CODE_ADRESSE + adress_conter
            )

            new_adress = code_if.count(" ") + code_if.count("!smart_call_func|") * 13 + code_if.count("!smart_tmp:goto|") * 3 - code_if.count("!smart_tmp:goto|")

            hex_adress_if = hex(CODE_ADRESSE + adress_conter + new_adress)[2:].upper()
            hex_adress_if = "0" * (4 - len(hex_adress_if)) + hex_adress_if
            hex_adress_if = hex_adress_if[2:] + " " + hex_adress_if[:2]


            code_compile = code_compile.format(hex_adress_if)

            adress_conter += new_adress
            code_compile += code_if

            last_if = True

            line_conter += 1    # add the line conter because continue
            continue

        elif line.lstrip().startswith("elif"):
            line_2 = replace_code(line, " ", "")[4:]

            if not line_2.endswith("{"):
                raise SmartError("On elif bloc, expected '{'", line_conter)
            else:
                line_2 = line_2[:-1]


            bloc_code, bloc_line = get_bloc(line_conter, code, error_message="On elif bloc")

            jump_line = bloc_line - line_conter - 1
            
            code_compile += "AD E9 02 C9 01 D0 !smart_tmp:elif "
            adress_conter += 7

            value_tmp = set_one_A_value(line_2)

            code_compile += value_tmp

            delta_branch = hex(value_tmp.count(" ") + value_tmp.count("!smart_call_func|") * 13 + 9)[2:].upper()

            code_compile = code_compile.replace("!smart_tmp:elif", delta_branch)

            code_compile += "C9 00 D0 08 A9 01 8D E9 02 4C {} A9 00 8D E9 02 "

            adress_conter += 17

            code_elif = compile_smarty(
                make_file=False,
                function_mode={"function_mode":True, "source_code":bloc_code, "global_function":function_name_usr, "global_function_replace":function_replace, "function_caller_ctx":caller_ctx, "global_var":smart_var, "smart_func":None, "if_mode":True, "global_goto":go_to, "goto_replace":go_to_replace, "while_mode":function_mode["while_mode"] if "while_mode" in function_mode else False},
                CODE_ADRESSE=CODE_ADRESSE + adress_conter
            )

            new_adress = code_elif.count(" ") + code_elif.count("!smart_call_func|") * 13 + code_elif.count("!smart_tmp:goto|") * 3 - code_elif.count("!smart_tmp:goto|")

            hex_adress_elif = hex(CODE_ADRESSE + adress_conter + new_adress)[2:].upper()
            hex_adress_elif = "0" * (4 - len(hex_adress_elif)) + hex_adress_elif
            hex_adress_elif = hex_adress_elif[2:] + " " + hex_adress_elif[:2]


            code_compile = code_compile.format(hex_adress_elif)

            adress_conter += new_adress
            code_compile += code_elif

            last_if = True

            line_conter += 1    # add the line conter because continue
            continue
        
        elif line.lstrip().startswith("else"):
            if not last_if:
                raise SmartError("'else bloc' was used but 'if bloc' was not created.")
            
            line_2 = replace_code(line, " ", "")[4:]

            if not line_2.endswith("{"):
                raise SmartError("On else bloc, expected '{'", line_conter)

            bloc_code, bloc_line = get_bloc(line_conter, code, error_message="On else bloc")

            jump_line = bloc_line - line_conter - 1
            
            code_compile += "AD E9 02 C9 00 D0 03 4C {} "
            adress_conter += 10

            code_else = compile_smarty(
                make_file=False,
                function_mode={"function_mode":True, "source_code":bloc_code, "global_function":function_name_usr, "global_function_replace":function_replace, "function_caller_ctx":caller_ctx, "global_var":smart_var, "smart_func":None, "if_mode":True, "global_goto":go_to, "goto_replace":go_to_replace, "while_mode":function_mode["while_mode"] if "while_mode" in function_mode else False},
                CODE_ADRESSE=CODE_ADRESSE + adress_conter
            )

            new_adress = code_else.count(" ") + code_else.count("!smart_call_func|") * 13 + code_else.count("!smart_tmp:goto|") * 3 - code_else.count("!smart_tmp:goto|")

            hex_adress_else = hex(CODE_ADRESSE + adress_conter + new_adress)[2:].upper()
            hex_adress_else = "0" * (4 - len(hex_adress_else)) + hex_adress_else
            hex_adress_else = hex_adress_else[2:] + " " + hex_adress_else[:2]


            code_compile = code_compile.format(hex_adress_else)

            adress_conter += new_adress
            code_compile += code_else
        
        elif line.lstrip().startswith("while"):
            line_2 = replace_code(line, " ", "")[5:]

            if not line_2.endswith("{"):
                raise SmartError("On while bloc, expected '{'", line_conter)
            else:
                line_2 = line_2[:-1]
            
            while_adress = hex(CODE_ADRESSE + adress_conter)[2:].upper()
            while_adress = "0" * (4 - len(while_adress)) + while_adress
            while_adress = while_adress[2:] + " " + while_adress[:2] + " "

            code_compile += set_one_A_value(line_2)

            bloc_code, bloc_line = get_bloc(line_conter, code, error_message="On while bloc")

            jump_line = bloc_line - line_conter - 1
            
            code_compile += "C9 00 D0 03 4C {} "
            adress_conter += 7

            code_while = compile_smarty(
                make_file=False,
                function_mode={"function_mode":True, "source_code":bloc_code, "global_function":function_name_usr, "global_function_replace":function_replace, "function_caller_ctx":caller_ctx, "global_var":smart_var, "smart_func":None, "if_mode":True, "global_goto":go_to, "goto_replace":go_to_replace, "while_mode":True},
                CODE_ADRESSE=CODE_ADRESSE + adress_conter
            )

            new_adress = code_while.count(" ") + code_while.count("!smart_call_func|") * 13 + code_while.count("!smart_tmp:goto|") * 3 - code_while.count("!smart_tmp:goto|")

            adress_conter += new_adress
            code_compile += code_while

            code_compile += "4C " + while_adress
            adress_conter += 3

            end_adress = hex(CODE_ADRESSE + adress_conter)[2:].upper()
            end_adress = "0" * (4 - len(end_adress)) + end_adress
            end_adress = end_adress[2:] + " " + end_adress[:2]

            code_compile = code_compile.format(end_adress).replace("! smart:break", end_adress)
        
        elif line.lstrip().startswith("break"):
            if not on_loop:
                raise SmartError("Error: 'break' keyword can only be used inside a loop.", line_conter)
        
            code_compile += "4C ! smart:break "     # set space on placeholder for conting adress
            adress_conter += 3

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

            function_name_usr[func_name] = smart_obj.SmartFunction(func_name, func_code)

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
            if function_mode["function_mode"]:
                if function_mode["if_mode"]:
                    raise SmartError("Can't import a module on a bloc.")
                else:
                    raise SmartError("Can't import a module on function.", line_conter)
            
            
            line_import = split_code(line, " ")[1:]

            try:

                if len(line_import) == 1:   # search in all directory
                    if not(line_import[0].startswith('"') and line_import[0].endswith('"')):
                        raise SmartError("Need a str value for path, in import.", line_conter)
                    name_import = line_import[0][1:-1]
                    import_info = import_tool.import_all(name_import, CODE_ADRESSE + adress_conter)


                elif len(line_import) == 3: # search in a spesific directory (smart, lib or path of code)
                    line_from = split_code("".join(line_import), "from")

                    if len(line_from) != 2:
                        raise SmartError("Sintaxe error: excepted 'from'.", line_conter)

                    name_import, type_import = line_from

                    if not(name_import.startswith('"') and name_import.endswith('"')):
                        raise SmartError("Need a str value for path, in import.", line_conter)
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
                if me.recursion:
                    raise CompileError(f"Compile fail: error with module, maybe a module import self... (error in {me.module_name})")
                else:
                    raise SmartError("Error during importing module:\n" + str(me))
                
            adress_delta = import_info.binary.count(" ")

            code_compile += import_info.binary
            adress_conter += adress_delta

            function_name_usr |= import_info.function
            smart_var |= import_info.variables


            adress_conter += 2

            new_adress_module = adress_for_RAM(CODE_ADRESSE + adress_conter) + " "

            code_compile = code_compile.replace("!smart_module_goto", new_adress_module)
            
            

        elif re.match(FUNCTION_PATTERN, line):     # function

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


                    value_str = get_str(smart_str)

                    for char in get_char_from_str(value_str):
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
            
            elif function_name in SmartBuiltIn.BUILT_IN_NAME_RETURN:
                logging.warning(f"'{function_name}' function is a return-function, but was used as a function.")
                
                match function_name:
                    case "input":
                        SmartBuiltIn.smartInput()


            elif function_name in function_name_usr:

                if function_name_usr[function_name].return_value:
                    logging.warning(f"Function '{function_name}' is a return-function but was used as a function.")

                # use a goto

                adress_conter += 13

                text_code = f"!smart_call_func|{function_name}|{caller_ctx}|{adress_conter}"

                function_replace.append(text_code)

                code_compile += text_code

            
            else:
                raise SmartError(f"Function '{function_name}' not exist.", line_conter)
        
        else:
            raise SmartError("Smart invalid syntaxe", line_conter)

        line_conter += 1

        last_if = False
        
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

    if (not function_mode["function_mode"]) and (not module_mode):
        for name, f in function_name_usr.items():
            if not f.called_function:
                logging.warning(f"Function '{name}' was never called.")

    # set the goto:

    if not function_mode["if_mode"]:
        for goto in go_to_replace:
            goto_name = goto.split("|")[1]

            try:
                adress = go_to[goto_name].adress
                    
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