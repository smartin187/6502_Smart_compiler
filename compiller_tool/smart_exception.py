# -*- coding: utf-8 -*-

"""
The exceptions of Smart.
Has:
- CompileError: for error with compile (file not found, module error...)
- SmartError: for syntax error or other problem with Smart language.
"""


import logging
from compiller_tool.color_tool import ColoredFormatter
from compiller_tool import compiller_data_run

line_of_instruction = None

def config_exception(_line_of_instruction) -> None:
    """Add the line_of_instruction function to the module."""
    global line_of_instruction
    line_of_instruction = _line_of_instruction

def confirm_user(log_message:str, error_reply:str="N", defaut:str="N", error_message:str="Aborted by user request.", line_counter:int=0) -> None:
    """Log an error asking the user a question (Y/N).
    Arg:
    - log_message: the message to log
    - error_reply: can be Y or N (UPPERCASE), the user's reply that raises SmartError
    - defaut: the default reply if the user does not reply
    - error_message: the message for the raised SmartError, used only if the user replies with `error_reply`
    - line_counter: the line number.
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
        print("Unknown reply!")
        confirm_user(log_message, error_reply, error_message, line_counter)

class CompileError(Exception):
    """An error during compilation (file not found, unknown error...).
    Use SmartError for errors in the code (syntax, bad value...)"""
    def __init__(self, message:str="Error"):
        logging.critical(message)

        self.error = message

class SmartError(CompileError):
    """The error for Smart (syntax error)."""
    def __init__(self, message:str, nb_instruction:int=0, set_error:bool=True):
        """Error for Smart language. Arg:
        - message: the error message
        - nb_instruction: the number of the instruction (used to find the line)
        - set_error: if True, print the error in red on console (default True)"""


        nbline, line_error = line_of_instruction(nb_instruction)

        if compiller_data_run.warning_endline[0]:
            module_name = "* (main_module)" if compiller_data_run.warning_endline[2] == "*" else compiller_data_run.warning_endline[2]
            text_endline = ColoredFormatter.COLORS["WARNING"] + f"Maybe you forget ';' at {compiller_data_run.warning_endline[1]} line, on {module_name}?"
        else:
            text_endline = ""

        if set_error:
            logging.critical(ColoredFormatter.COLORS["CRITICAL"] + "Error during build:")
            print(f"~~~~~~~~~~\nAt {nbline} line:\n{line_error}\n~~~~~~~~~~\nError :\n{message}\n{text_endline}\n{ColoredFormatter.RESET}")

        self.syntaxerror = message
        self.nbline = nbline


class ModuleError(CompileError):
    """Exception for a module (file not found, recursion error...)"""
    def __init__(self, message:str="", recursion:bool=False, module_name:str="", no_error:bool=False):
        self.recursion = recursion
        self.module_name = module_name

        if not no_error:
            super().__init__(message)