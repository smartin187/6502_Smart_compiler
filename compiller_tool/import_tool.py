import os
from pathlib import Path

compile_smarty = None

class ModuleError(Exception):
    pass

class ModuleInfo:
    """A class used from compile_smarty for get the variable and function name + binary code."""
    def __init__(self, binary:str, variable:dict, function:dict):
        self.binary = binary
        self.variables = variable
        self.function = function
    

def config_import(_compile_smarty) -> None:
    """Get dependence from smart_compiller.py"""
    global compile_smarty
    compile_smarty = _compile_smarty


def import_module(file_name:str, start_adress:int) -> ModuleInfo:
    """Import a module from name (path can be relative of abs)."""
    path = os.path.abspath(file_name)

    if not Path(path).is_file():
        raise ModuleError(f"File '{path}' not exist!")

    module_info:ModuleInfo = compile_smarty(
        file=path,
        CODE_ADRESSE=start_adress,
        make_file=False,
        module_mode=True
    )

    module_info.binary = module_info.binary.split(":")[1].lstrip()

    return module_info

    

def import_lib(file_name:str, start_adress:int) -> ModuleInfo:raise Exception("Not implemented")

def import_smart(file_name:str, start_adress:int) -> ModuleInfo:raise Exception("Not implemented")

def import_all(file_name:str, start_adress:int) -> ModuleInfo:raise Exception("Not implemented")