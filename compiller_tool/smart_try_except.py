# -*- coding: utf-8 -*-

"""
This module has functions for try/except in Smart.
"""

from compiller_tool.smart_exception import SmartError

def control_except(after_try_bloc: bool, on_try_bloc: bool, line_counter:int) -> int:
    """
    This function is used to test if an except block follows a try block.
    """
    if after_try_bloc:
        after_try_bloc = False

    else:
        if on_try_bloc:
            raise SmartError("Try block was created but except block not exist.", line_counter)

    return after_try_bloc



