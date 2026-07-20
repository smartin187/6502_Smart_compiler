# -*- coding: utf-8 -*-

"""
This module is not used for compilation, but for help debug.
You can set the function of asm_tool on the compiller for debuging.

On compiller, it is used for warning.
"""

from compiller_tool import color_tool
from compiller_tool.compiller_data_run import SMART_PLACEHOLDER

def get_adress(code_compile:str) -> int:
    """Return the adress offset from the start of programme from a hex code."""
    offset_adress = code_compile.count(" ") + 13 * code_compile.count("!smart_call_func|") + code_compile.count("!smart_tmp:goto|") * 3 - code_compile.count("!smart_tmp:goto|")

    if code_compile.startswith("0400: "):
        offset_adress -= 1
    
    return offset_adress

def verryfing_adress_conter(adress_conter:int, code_compile:str, not_print:bool=False) -> bool | None:
    """This function is used to verify the adress_conter and the code_compile.
    Use this function is the adress_conter is not good. Test on the compiller
    Return None if double space on code.
    """

    normal_adress = get_adress(code_compile)

    if "  " in code_compile:

        double_space = code_compile.count("  ")

        double_space_placeholder = 0
        for placeholder in SMART_PLACEHOLDER:
            double_space_placeholder += code_compile.count(placeholder)
        
        double_space -= double_space_placeholder

        if double_space != 0:

            if not not_print:
                print(color_tool.Colors.RED, "verryfing_adress_conter: error. code_compile have double space.", color_tool.Colors.RESET)
            
            return None

    if adress_conter != normal_adress:
        if not not_print:
            print(color_tool.Colors.RED, "verryfing_adress_conter: error. Normal adress:", normal_adress, "\nadress_conter:", adress_conter, color_tool.Colors.RESET)
        return False
    
    else:
        if not not_print:
            print(color_tool.Colors.GREEN, "verryfing_adress_conter: adress_conter is good.", color_tool.Colors.RESET)

    return True


verryfing_adress_conter_no_print = lambda adress_conter, code_compile: verryfing_adress_conter(adress_conter, code_compile, not_print=True)
