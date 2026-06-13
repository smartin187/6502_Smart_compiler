# -*- coding: utf-8 -*-

"""
This module have the Smart object class:
- SmartObj
- SmartFunction
- SmartVariable
- SmartGoto
"""

from compiller_tool.string_tool import in_code
from compiller_tool.smart_exception import SmartError


class SmartObj:
    def __init__(self, name:str):
        self.name = name
    
class ReservedAdress(SmartObj):
    """Information about a reserved adress (adress). Used for adress for str value."""
    def __init__(self, adress:str):
        super().__init__(name="ReservedAdress")

        self.adress = adress

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

class SmartVariable(SmartObj):
    """Information about a variable (name and adress on RAM)."""
    def __init__(self, name:str, ram_adress:str):
        super().__init__(name)

        self.ram_adress = ram_adress


class SmartGoto(SmartObj):
    """Information about a goto (name and adress)."""
    def __init__(self, name:str, adress:str):
        super().__init__(name)

        self.adress = adress

SIZE_ADVANCED_OBJ = 0x15

class AdvancedObj(SmartObj):
    """Information about an advanced object (str).
    Use multi-byte
    """
    def __init__(self, name:str, adress:str, size:int=SIZE_ADVANCED_OBJ):
        super().__init__(name)

        self.ram_adress = adress
        self.size = size

class SmartStr(AdvancedObj):
    """Information about a string (name and adress)."""
    def __init__(self, name:str, adress:str):
        super().__init__(name, adress)
    
    def get_index(self, line:str, test_mode:bool=False) -> int:
        """Return the index from the line."""
        if "[" not in line or "]" not in line:
            raise SmartError(f"Invalid syntax for '{line.split('=')[0]}', expected an index between brackets [].", set_error=not test_mode)

        index = int(line.split("=")[0].split("[")[1].replace("]", ""))

        if index >= SIZE_ADVANCED_OBJ:
            raise SmartError(f"Index out of range for '{line.split('=')[0]}', max index is {SIZE_ADVANCED_OBJ - 1}.", set_error=not test_mode)

        elif index < -SIZE_ADVANCED_OBJ:
            raise SmartError(f"Index out of range for '{line.split('=')[0]}', min index is {-SIZE_ADVANCED_OBJ}.", set_error=not test_mode)
    
        if index < 0:
            index = SIZE_ADVANCED_OBJ + index
        
        return index

    def get_adress_from_index(self, index:int) -> str:
        """Return the adress of the character at the given index."""
        return self.ram_adress + index
