# -*- coding: utf-8 -*-

"""
This module has the Smart object classes:
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
    """Information about a reserved address. Used for the address of str values."""
    def __init__(self, adress:int):
        super().__init__(name="ReservedAdress")

        self.adress = adress

class SmartFunction(SmartObj):
    """Information about a smart function."""
    def __init__(self, name:str, func_code:str, parameters:list[str]):
        """Set the attributes of the function."""
        super().__init__(name)

        self.source_code_function = func_code
        self.code_compile_f = ""
        self.function_adress = 0
        self.return_value = in_code("return ", self.source_code_function)
        self.parameters = parameters

        self.called_function = False    # if False at the end of build, the function was never called

class SmartVariable(SmartObj):
    """Information about a variable (name and address on RAM)."""
    def __init__(self, name:str, ram_adress):
        super().__init__(name)

        self.ram_adress = ram_adress


class SmartGoto(SmartObj):
    """Information about a goto (name and address)."""
    def __init__(self, name:str, adress:str):
        super().__init__(name)

        self.adress = adress

SIZE_ADVANCED_OBJ = 0x15

class AdvancedObj(SmartObj):
    """Information about an advanced object (str).
    Uses multiple bytes.
    """
    def __init__(self, name:str, adress:int, size:int=SIZE_ADVANCED_OBJ):
        super().__init__(name)

        self.ram_adress = adress
        self.size = size

class SmartStr(AdvancedObj):
    """Information about a string (name and address)."""
    def __init__(self, name:str, adress:str):
        super().__init__(name, adress)


    def get_index(self, line:str, test_mode:bool=False) -> tuple[bool, int | str]:
        """Return the index from the line.
        Return: tuple[
            bool: if the value is a literal value (True) or a variable / expression (False),
            int | str: the index (int) or the variable / expression (str)
        ]
        """
        if "[" not in line or "]" not in line:
            raise SmartError(f"Invalid syntax for '{line.split('=')[0]}', expected an index between brackets [].", set_error=not test_mode)

        value = line.split("=")[0].split("[")[1].replace("]", "")

        try:
            index = int(value)
        except ValueError:
            return False, value

        if index >= SIZE_ADVANCED_OBJ:
            raise SmartError(f"Index out of range for '{line.split('=')[0]}', max index is {SIZE_ADVANCED_OBJ - 1}.", set_error=not test_mode)

        elif index < -SIZE_ADVANCED_OBJ:
            raise SmartError(f"Index out of range for '{line.split('=')[0]}', min index is {-SIZE_ADVANCED_OBJ}.", set_error=not test_mode)

        if index < 0:
            index = SIZE_ADVANCED_OBJ + index

        return True, index

    def get_adress_from_index(self, index:int) -> str:
        """Return the address of the character at the given index."""
        return self.ram_adress + index
