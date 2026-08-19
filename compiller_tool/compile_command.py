# -*- coding: utf-8 -*-

"""
This module is for the compiletime keyword
"""
import logging
from compiller_tool.smart_exception import SmartError

from compiller_tool.compiller_data_run import reset_define
from compiller_tool import compiller_data_run
from compiller_tool.string_tool import good_variable_name

define = {}     # the define are stored in this dict

reset_define(define)

def get_line_debug(line:str) -> str:
    """Return the line for the debug if debug mode is enabled. Return '' if debug mode is disabled."""
    if compiller_data_run.debug_max:

        line_debug = []

        line = line.upper().strip()

        for char in line:
            if char in compiller_data_run.BASE_ALLOW_CHAR:
                line_debug.append(char)
            else:
                line_debug.append("?")

        # make hex prorgam:
        hex_programm = []
        for char in line_debug:
            hex_programm.append(f"A9 {hex(ord(char))[2:].upper()} 20 EF FF ")

        hex_programm.append(f"A9 0D 20 EF FF ") # set a \r at the end

        return "".join(hex_programm)
    
    return ""

def compiletime_command(line:str, smart_var:dict) -> None:
    """This function is for use the compiletime command."""

    line = line[len("compiletime "):].strip()

    if line.startswith("define "):   # define a code to replace
        new_define = line[len("define "):].strip()

        if new_define.count(" to ") != 1:
            raise SmartError("Invalid compiletime command: expected a name and a value after 'define' keyword.")

        name, value = new_define.split(" to ")

        name = name.strip()
        value = value.strip()

        if name in define:
            logging.warning(f"Redefining compiletime define '{name}' from '{define[name]}' to '{value}'.")

        define[name] = value

    elif line.startswith("debug "):  # set the debug mode
        debug_value = line[len("debug "):].strip()

        if debug_value in ("True", "1"):
            compiller_data_run.debug_max = True
            logging.info("Debug mode is enabled; All lines will be printed during execution.")
        elif debug_value in ("False", "0"):
            compiller_data_run.debug_max = False
            logging.info("Debug mode is disabled.")
        else:
            raise SmartError("Invalid compiletime command: expected 'True' or 'False' or 1 or 0 after 'debug' keyword.")

    elif line.startswith("realloc "):  # realloc a variable (= rename a variable)
        realloc_value = line[len("realloc "):].strip()

        try:
            old_var, new_var = realloc_value.split(" to ")
        except:
            raise SmartError("Invalid sintaxe after 'realloc': excepted oldvar to newvar.")

        try:
            base_name_old = old_var.replace(" ", "")[1:]
            base_name_new = new_var.replace(" ", "")[1:]
        except:
            raise SmartError("Invalid sintaxe for name of variable in realloc.")

        if not good_variable_name(base_name_old):
            raise SmartError(f"Invalid sintaxe '{base_name_old}' for realloc (excepted variable name).")
        elif not good_variable_name(base_name_new):
            raise SmartError(f"Invalid sintaxe '{base_name_new}' for realloc (excepted variable name).")

        if base_name_old not in smart_var:
            raise SmartError(f"Variable '{base_name_old}' not found for realloc.")

        if base_name_new == base_name_old:
            raise SmartError(f"Variable '{base_name_new}' is the same as '{base_name_old}', you can't set a realloc.")

        var_object = smart_var[base_name_old]

        var_object.name = base_name_new

        smart_var[base_name_new] = var_object
        del smart_var[base_name_old]

    else:
        raise SmartError("Excepted keyword after 'compiletime'.")



