# -*- coding: utf-8 -*-

"""
The compiller for smart.

Fonction: compile_smarty for start the compile of a smart code.
"""

import traceback
from pathlib import Path
import os
import logging

logging.basicConfig(format="SmartCompiller %(levelname)s: %(message)s", level=logging.INFO)

logging.info("Starting compiller...")


class SmartError(Exception):
    """The error for Smart (syntaxe error)."""
    def __init__(self, message:str, nb_instruction:int=0):
        logging.error("\033[31mError during build:")

        nbline, line_error = line_of_instruction(nb_instruction)

        print(f"~~~~~~~~~~\nAt {nbline} line:\n{line_error}\n~~~~~~~~~~\nError :\n{message}\n\033[0m")

        self.syntaxerror = message
        self.nbline = nbline

        

code_line = None

line_of_instruction = None

def compile_smarty(file:str="", argv:list | tuple=[], START_ADRESSE:str="0400: ", CODE_ADRESSE:int=0x400, make_file:bool=True, function_mode:tuple[bool, str]=(False, "")) -> None:
    """Start the compile from file."""
    global line_of_instruction, code_line

    def line_of_instruction(nb_instruction:int) -> tuple[int, str]:
        """Return the number of line and the line of the instruction."""
        nb = 0
        line_counter = 0

        for line in code_line:

            nb += line.count(";")

            line_counter += 1

            if nb_instruction + 1 <= nb:
                return (line_counter + 1, code_line[line_counter-1])



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
    
    def set_one_A_value(value:str, one_addition:bool=False) -> str:
        """Return the value for set one A."""
        if "+" in value:    # addition
            try:
                value_1, value_2 = value.split("+", 1)
              
                hex_value_2 = set_one_A_value(value_2, one_addition=True)

                if hex_value_2.startswith("6D "):
                    asm = f"{set_one_A_value(value_1)}18 {hex_value_2}"

                else:
                    asm = f"{set_one_A_value(value_1)}18 69 {hex_value_2[3:]}"

                return asm

            except SmartError as se:
                raise SmartError(str(se), se.nbline)

            except:
                print(traceback.format_exc())
                raise SmartError(f"Error with math '+' : '{value}'", line_conter)

        elif value[0] == ".":
            variable = value[1:]

            if variable not in smart_var:
                raise SmartError(f"Name error : name '{value}' is not defined.", line_conter)
            
            if not one_addition:
                return f"AD {adress_for_RAM(smart_var[variable])} "
            else:
                return f"6D {adress_for_RAM(smart_var[variable])} "
        
        elif len(value) == 2:
            control_hex(value)
            return "A9 " + value + " "
        
        elif value[0] == "'":
            return "A9 " + get_char(value) + " "
    
        elif value[0] == "\"":
            raise SmartError(f"Smart forbiden value: '{value}'", line_conter)

    
        else:
            raise SmartError(f"Smart value error: {value}", line_conter)

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
        - Any letter (A-Z, a-z). Special letter (éèëù...) are accepted.
        - Any number 0-9
        - underscore _"""
        for char in name:
            if not (char.isalpha() or char.isdigit() or char == "_"):
                return False
        return True

    # -----------

    ACUMULATOR_REGISTER = "AXY"

    # -----------

    smart_var = {}
    adress_var = 0x300

    line_conter = 0

    code_compile = START_ADRESSE if not function_mode[0] else ""

    go_to = {}
    function_smart = {}

    go_to_replace = []
    function_replace = []

    adress_conter = 0

    if function_mode[0]:
        code_line = function_mode[1].split("\n")
    else:
        sma = open(file, "r", encoding="UTF-8")

        code_start = sma.read()

        sma.close()

        code_line = code_start.split("\n")

    code = ""

    for line in code_line:
        line_tmp = line.split("//")[0] + "\n"
        code += line_tmp.lstrip(" ")

        
    

    code = code.replace("\n", "").split(";")#.replace(" ", "").split(";")

    logging.info("Buiilding asm")

    jump_line = 0

    for line in code:

        if jump_line:
            jump_line -= 1
            continue

        if line == "":
            line_conter += 1
            logging.warning("Empty line detected.")
            continue


        if line[0] in ACUMULATOR_REGISTER:
            line = line.replace(" ", "")
            read_line = line.split("=")
            

            r = read_line[0]

            if len(read_line) != 2:
                raise SmartError(f"Smart syntaxe error:\nline {line_conter}", line_conter)
        

            
            code_compile += set_one_A_value(read_line[1]) if r == "A" else "A2" + set_one_A_value(read_line[1])[2:] if r == "X" else "A0" + set_one_A_value(read_line[1])[2:]

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

            var_name, value = line.split("=")

            if not good_variable_name(var_name):
                raise SmartError(f"Bad variable name : '{var_name}'", line_conter)

            if var_name not in smart_var: # make new variable
                if len(smart_var) >= 256:
                    raise SmartError("Memory error : maximum variable are 256.", line_conter)
                smart_var[var_name] = adress_var
                adress_var += 1
            
            value_RAM = set_one_A_value(value)
                        
            code_compile += f"{value_RAM}8D {adress_for_RAM(smart_var[var_name])} "

            adress_conter += 5

            logging.info(f"Build asm command: using RAM for variable '{var_name}'")
        
        elif line.startswith("void "):      # make fonction
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

            while True:
                if code[funciton_line].startswith("}"):
                    code[funciton_line] = code[funciton_line][1:]
                    break

                else:
                    func_code += code[funciton_line] + ";"
                    funciton_line += 1
            
            function_smart[func_name] = compile_smarty(make_file=False, function_mode=(True, func_code), CODE_ADRESSE=0x400 + adress_conter)

            jump_line = funciton_line - line_conter - 1

            logging.debug(f"'{func_name}' has been created.")
            

        else:     # function

            line = line.replace(" ", "")

            function_name, function_arg = line.split(":")
            function_arg = function_arg.split(",")

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

                        adress_conter += 5
                
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

            elif function_name in function_smart:
                func_code_tmp = function_smart[function_name]

                # use a goto

                adress_conter += 13

                text_code = f"!smart_call_func|{function_name}|{adress_conter}"

                function_replace.append(text_code)

                code_compile += text_code

                #adress_conter += func_code_tmp.count(" ")

            
            else:
                raise SmartError(f"Function '{function_name}' not exist.", line_conter)

        line_conter += 1
    
    if not function_mode[0]:
        code_compile += "00 "
    else:
        code_compile += "4C 00 00 "
    
    # set the function:

    function_adress = {}

    for function in function_smart:
        function_adress[function] = adress_conter

        code_func = function_smart[function]
        
        code_compile += code_func

        adress_conter += code_func.count(" ")

    # call function

    for function in function_replace:
        function_name_tmp, r_adress = function.split("|")[1:]

        adress_func = CODE_ADRESSE + function_adress[function_name_tmp] + 1

        hex_adress_function = hex(adress_func)[2:].upper()

        hex_adress_function = "0" * (4 - len(hex_adress_function)) + hex_adress_function

        hex_adress_function = f"{hex_adress_function[2:]} {hex_adress_function[:2]}"

        return_aress = hex(adress_func + function_smart[function_name_tmp].count(" ") - 1)[2:].upper()
        return_aress = "0" * (4 - len(return_aress)) + return_aress


        return_aress_2 = hex(adress_func + function_smart[function_name_tmp].count(" ") - 2)[2:].upper()
        return_aress_2 = "0" * (4 - len(return_aress_2)) + return_aress_2

        r_adress = hex(int(r_adress) + CODE_ADRESSE)[2:].upper()
        r_adress = "0" * (4 - len(r_adress)) + r_adress


        #code_compile = code_compile.replace(function, f"A9 {r_adress[:2]} 8D {return_aress[2:]} {return_aress[:2]} A9 {r_adress[2:]} 8D {return_aress_2[:2]} {return_aress_2[2:]} 4C {hex_adress_function} ")
        code_compile = code_compile.replace(function, f"A9 {r_adress[:2]} 8D {return_aress[2:]} {return_aress[:2]} A9 {r_adress[2:]} 8D {return_aress_2[2:]} {return_aress_2[:2]} 4C {hex_adress_function} ")

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