# -*- coding: utf-8 -*-

"""
This module is for the compiletime keyword
"""
import logging
from compiller_tool.smart_exception import SmartError

from compiller_tool.compiller_data_run import reset_define

define = {}     # the define are stored in this dict

reset_define(define)

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

    else:
        raise SmartError("Excepted keyword after 'compiletime'.")



