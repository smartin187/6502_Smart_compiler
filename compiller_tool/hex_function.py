# -*- coding: utf-8 -*-

"""
This module has the function build_asm_entry used by the Smart built-in function asm_entry.
"""
import logging
from compiller_tool.smart_exception import SmartError
from compiller_tool.string_tool import adress_for_RAM
from compiller_tool import compiller_data_run

set_on_A_value = None

def config_hex_function(_set_on_A_value) -> None:
    """Add for hex_function.py the function set_on_A_value."""
    global set_on_A_value
    set_on_A_value = _set_on_A_value

def good_asm(asm:str) -> bool:
    """Return True if assembly is valid.
    Assembly is valid if chars are in A-F 0-9"""
    for char in asm:
        if char not in "ABCDEF0123456789":
            return False
    return True

def build_asm_entry(function_arg:list, line_conter:int, get_str_function, adress_conter:int, smart_var:dict, START_ADRESS:int) -> str:
    """This function returns the hex for an asm_entry function."""
    if len(function_arg) != 1:
        raise SmartError("Function asm_entry take 1 arg.", line_conter)

    asm = function_arg[0]

    asm_str = get_str_function(asm).strip(" ").replace(" ", "")

    if len(asm_str) == 0:
        logging.warning(f"Empty assembly entry, at line {line_conter}")

    # replace the hex value with @

    to_replace = []

    # do the replace for the variable address:
    for i, char in enumerate(asm_str):
        if char == "@":
            escape_sequence = asm_str[i:]

            if escape_sequence.startswith("@var_adress:"):
                var_name = escape_sequence.split(":", 1)[1].split("|", 1)[0]

                var_prefix = var_name[0]

                var_name = var_name[1:]

                if var_name not in smart_var:
                    raise SmartError(f"Variable {var_name} not found.", line_conter)

                var_adress = smart_var[var_name].ram_adress

                to_replace.append((f"@var_adress:{var_prefix}{var_name}|", adress_for_RAM(var_adress)))

            elif escape_sequence.startswith("@adress+") or escape_sequence.startswith("@adress-"):

                operator = escape_sequence[7]

                number = escape_sequence.split(operator, 1)[1].split("|", 1)[0]

                if not number.isdigit():
                    raise SmartError(f"Invalid number `{number}` for asm_entry.")

                number_int = int(number)

                if operator == "+":
                    replace_adress = adress_conter + START_ADRESS + number_int
                else:
                    replace_adress = adress_conter + START_ADRESS - number_int

                to_replace.append((f"@adress{operator}{number}|", adress_for_RAM(replace_adress)))


    for old, new in to_replace:
        asm_str = asm_str.replace(old, new)

    asm_str = asm_str.replace("@adress", adress_for_RAM(adress_conter + START_ADRESS))

    asm_str = asm_str.replace(" ", "")

    if ((len(asm_str) % 2) != 0) or (not good_asm(asm_str)):
        raise SmartError(f"Invalid assembly entry, bad bytes was given.", line_conter)

    return " ".join(asm_str[i:i+2] for i in range(0, len(asm_str), 2)) + " "


def make_error(error_value:str, try_mode:bool, set_need_error:bool=True, add_to_adress_conter:bool=True) -> tuple[str, int]:
    """
    Return a tuple with the op code for the runtime error and adress_conter.
    Return hex code.
    Add to address counter if the argument is True
    """
    #nonlocal address_counter
    address_counter = 0 # the lenght of hex code

    if try_mode:
        code_compile = "!  smart_error_try "
        if add_to_adress_conter:
            address_counter += 3

        return code_compile, address_counter

    else:

        code_compile = ""

        compiller_data_run.need_error = set_need_error

        code_compile += "A9 45 20 EF FF "     # print E
        if add_to_adress_conter:
            address_counter += 5

        code_compile += set_on_A_value(error_value, add_adress=add_to_adress_conter)

        code_compile += "4C !  smart_runtime_error"    # set 2 spaces on placeholder for counting address
        if add_to_adress_conter:
            address_counter += 3

        return code_compile, address_counter

def imediate_value(value:str) -> bool:
    """Return True if the value is an immediate value, False otherwise.
    A9 41 : immediate value (LDA #41)
    AD 00 04 : address value (LDA $0400)
    """
    try:
        start = value.replace(" ", "")[0:2]
    except IndexError:
        return False

    if start == "A9":
        return True
    return False
