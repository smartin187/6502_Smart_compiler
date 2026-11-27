# -*- coding: utf-8 -*-

"""
This module is used for the optimize mode.
"""
import logging
from compiller_tool.compiller_data_run import BASE_ALLOW_CHAR

MESSAGE_OPTIMIZE = "Try to optimize expression. Do Ctrl+c for cancel."

def optimize_expression(expression:str) -> str | None:
    """Optimize the expression if the result can be know at compile time. Return None if can't optimize."""
    # control if the value can be eval:
    expression = expression.replace(" ", "")

    # for the char value:       # it work, but for exemple: 'A''B' -> sintaxe error, but the programme optimize it.
    #for char in BASE_ALLOW_CHAR:
    #    expression = expression.replace(f"'{char}'", str(ord(char)))


    for char in expression:
        if char not in "0123456789+-*/%":
            return

    if "**" in expression:
        return

    if expression == "":
        logging.warning("Try to optimize an expression, but the expression is empty (value error: missing value)")

    # Carful: it can be a vulnerability.
    try:
        print(MESSAGE_OPTIMIZE, end="\r")
        optimized_value = eval(expression)
        print(" " * len(MESSAGE_OPTIMIZE), end="\r")

        if isinstance(optimized_value, float) and "/" in expression:
            optimized_value = int(optimized_value)

        elif not isinstance(optimized_value, int):
            return

        optimized_value %= 256

        optimized = str(optimized_value)



    except KeyboardInterrupt:
        print("Optimization canceled by user." + " " * len(MESSAGE_OPTIMIZE))
        return

    except:
        return

    if optimized == expression:   # if the expression is already optimized
        return

    return optimized

