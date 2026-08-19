# -*- coding: utf-8 -*-

"""
This module is for the compiletime keyword
"""
import logging
from compiller_tool.smart_exception import SmartError

from compiller_tool.compiller_data_run import reset_define
from compiller_tool import compiller_data_run

define = {}     # the define are stored in this dict

reset_define(define)

ALLOW_CHAR = "!\"#$%'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_ " # to use only 1 module

def get_line_debug(line:str) -> str:
    """Return the line for the debug if debug mode is enabled. Return '' if debug mode is disabled."""
    if compiller_data_run.debug_max:

        line_debug = []

        line = line.upper().strip()

        for char in line:
            if char in ALLOW_CHAR:
                line_debug.append(char)
            else:
                line_debug.append("?")

        #clean_line = "".join(line_debug)

        # make hex prorgam:
        hex_programm = []
        for char in line_debug:
            hex_programm.append(f"A9 {hex(ord(char))[2:].upper()} 20 EF FF ")

        return "".join(hex_programm)
    
    return ""

def compiletime_command(line:str) -> None:
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

    else:
        raise SmartError("Excepted keyword after 'compiletime'.")



