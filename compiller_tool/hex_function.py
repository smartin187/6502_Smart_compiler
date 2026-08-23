# -*- coding: utf-8 -*-

"""
This module have the function build_asm_entry used by the Smart built-in function asm_entry.
"""
import logging
from compiller_tool.smart_exception import SmartError

def good_asm(asm:str) -> bool:
    """Return True if assembly is good.
    Assembly is good if char is in A-F 0-9"""
    for char in asm:
        if char not in "ABCDEF0123456789":
            return False
    return True

def build_asm_entry(function_arg:list, line_conter:int, get_str_function) -> str:
    """This function return the hex for for an asm_entry function."""
    if len(function_arg) != 1:
        raise SmartError("Function asm_entry take 1 arg.", line_conter)
    
    asm = function_arg[0]

    asm_str = get_str_function(asm).strip(" ").replace(" ", "")

    if len(asm_str) == 0:
        logging.warning(f"Empty assembly entry, at line {line_conter}")
    

    if ((len(asm_str) % 2) != 0) or (not good_asm(asm_str)):
        raise SmartError(f"Invalid assembly entry, bad bytes was given.", line_conter)
    
    return " ".join(asm_str[i:i+2] for i in range(0, len(asm_str), 2)) + " "
