# -*- coding: utf-8 -*-

"""
This module have the Smart object class:
- SmartFunction
"""

from compiller_tool.string_tool import in_code

class SmartObj:
    def __init__(self, name:str):
        self.name = name

class SmartFunction(SmartObj):
    """Information about a smart function."""
    def __init__(self, name:str, func_code:str):
        """Set the attibute of the function."""
        super().__init__(name)
        
        self.source_code_function = func_code
        self.code_compile_f = ""
        self.function_adress = 0
        self.return_value = in_code("return ", self.source_code_function)

        self.called_function = False    # if False at the end of build, the function was never called



