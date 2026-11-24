# -*- coding: utf-8 -*-

"""
This module is used for the optimize mode.
"""

def optimize_expression(expression:str) -> str | None:
    """Optimize the expression if the result can be know at compile time. Return None if can't optimize."""
    # control if the value can be eval:
    expression = expression.replace(" ", "")
    for char in expression:
        if char not in "0123456789+-*/%":
            return

    # Carful: it can be a vulnerability.
    try:
        optimized_value = eval(expression)
        if isinstance(optimized_value, float) and "/" in expression:
            optimized_value = int(optimized_value)

        elif not isinstance(optimized_value, int):
            return
        
        optimized_value %= 256

        optimized = str(optimized_value)
        
    except:
        return

    if optimized == expression:   # if the expression is already optimized
        return

    return optimized
    
