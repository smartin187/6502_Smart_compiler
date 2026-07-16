# -*- coding: utf-8 -*-

"""
This module is not used for compilation, but for help debug.
You can set the function of asm_tool on the compiller for debuging.
"""

from compiller_tool import color_tool

def verryfing_adress_conter(adress_conter:int, code_compile:str) -> bool:
    """This function is used to verify the adress_conter and the code_compile.
    Use this function is the adress_conter is not good. Test on the compiller"""
    normal_adress = code_compile.count(" ") + 13 * code_compile.count("!smart_call_func|")

    if code_compile.startswith("0400: "):
        normal_adress -= 1

    if adress_conter != normal_adress:
        print(color_tool.Colors.RED, "verryfing_adress_conter: error. Normal adress:", normal_adress, "\nadress_conter:", adress_conter, color_tool.Colors.RESET)
        return False
    
    else:
        print(color_tool.Colors.GREEN, "verryfing_adress_conter: adress_conter is good.", color_tool.Colors.RESET)

    return True
        

