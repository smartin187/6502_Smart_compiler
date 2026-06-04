# -*- coding: utf-8 -*-

"""
The exception of smart.
Have:
- CompileError: for error with compile (file not found, module error...)
- SmartError: for sintaxe error or other probleme with Smart language.
"""


import logging
from compiller_tool.color_tool import ColoredFormatter
from compiller_tool import compiller_data_run

line_of_instruction = None

def config_exception(_line_of_instruction) -> None:
    """Add to module the line_of_instruction function."""
    global line_of_instruction
    line_of_instruction = _line_of_instruction

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

        if compiller_data_run.warning_endline[0]:
            module_name = "* (main_module)" if compiller_data_run.warning_endline[2] == "*" else compiller_data_run.warning_endline[2]
            text_endline = ColoredFormatter.COLORS["WARNING"] + f"Maybe you forget ';' at {compiller_data_run.warning_endline[1]} line, on {module_name}?"
        else:
            text_endline = ""

        print(f"~~~~~~~~~~\nAt {nbline} line:\n{line_error}\n~~~~~~~~~~\nError :\n{message}\n{text_endline}\n{ColoredFormatter.RESET}")

        self.syntaxerror = message
        self.nbline = nbline