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

def confirm_user(log_message:str, error_reply:str="N", defaut:str="N", error_message:str="Aborted by user request.", line_counter:int=0) -> None:
    """Set a error log for say a question for user (Y/N).
    Arg:
    - log_message: the message on log*
    - error_reply: can be Y or N (UPPERCASE), the reply of user raise SmartError
    - defaut: de defaut reply is user not reply
    - error_message: the message on raise SmartError, used only if the user reply by `error_reply`
    - line_counter: the number of line.
    """
    continue_reply = "N" if error_reply == "Y" else "Y"

    choos = f'({"N" if defaut == "N" else "n"}/{"Y" if defaut == "Y" else "y"}): '

    logging.error(log_message + choos, extra={'no_newline': True})
    reply = input().upper()

    if reply == "": # defaut
        reply = defaut

    if reply == error_reply:
        raise SmartError(error_message, line_counter)

    elif reply == continue_reply:
        pass
    
    else:
        print("Unknow reply!")
        confirm_user(log_message, error_reply, error_message, line_counter)

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


class ModuleError(CompileError):
    """Exception for module (file not found, recursion error...)"""
    def __init__(self, message:str="", recursion:bool=False, module_name:str=""):
        self.recursion = recursion
        self.module_name = module_name
        super().__init__(message)