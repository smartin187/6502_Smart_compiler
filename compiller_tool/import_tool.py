import os
from pathlib import Path
import sys

from compiller_tool.smart_exception import ModuleError
from compiller_tool.color_tool import Colors

compile_smarty = None

PATH_LIB = {
    "global":"/usr/lib/Smart-SmartyKit/global_lib/" if sys.platform == "linux" else os.path.join(os.environ["LOCALAPPDATA"], "Smart-SmartyKit\\lib\\global_lib\\"),
    "smart":"/usr/lib/Smart-SmartyKit/smart_lib/" if sys.platform == "linux" else os.path.join(os.environ["LOCALAPPDATA"], "Smart-SmartyKit\\lib\\smart_lib\\")
}

class ModuleInfo:
    """A class used from compile_smarty for get the variable and function name + binary code."""
    def __init__(self, binary:str, variable:dict, function:dict):
        self.binary = binary
        self.variables = variable
        self.function = function
    
def show_path_lib() -> None:
    """Show the path for the global and smart lib."""
    print(f"{Colors.GREEN}Lib path (for import from lib and smart):{Colors.RESET}",
        f"Global lib path: {PATH_LIB['global']}",
        f"Smart lib path: {PATH_LIB['smart']}",
        sep="\n"
    )


def control_lib() -> None:
    """Raise ModuleError if the path for the global and smart lib is missing."""
    if not Path(PATH_LIB["global"]).is_dir():
        raise ModuleError(f"Module error: global lib directory is missing. Path is '{PATH_LIB['global']}'")

    if not Path(PATH_LIB["smart"]).is_dir():
        raise ModuleError(f"Module error: smart lib directory is missing. Path is '{PATH_LIB['smart']}'")


def config_import(_compile_smarty) -> None:
    """Get dependence from smart_compiller.py"""
    global compile_smarty
    compile_smarty = _compile_smarty

def get_module(path:str, start_adress:int) -> ModuleInfo:
    """Return the ModuleInfo from a path."""
    try:
        module_info:ModuleInfo = compile_smarty(
            file=path,
            CODE_ADRESSE=start_adress,
            make_file=False,
            module_name=path
        )

        module_info.binary = module_info.binary.split(":")[1].lstrip()

        return module_info
    
    except RecursionError:
        raise ModuleError("Error during compiling module. Maybe a module have import it?", recursion=True, module_name=path)

def import_module(file_name:str, start_adress:int, no_error:bool=False) -> ModuleInfo:
    """Import a module from name (path can be relative of abs)."""
    path = os.path.abspath(file_name)

    if not Path(path).is_file():
        raise ModuleError(f"File '{path}' not exist!", no_error=no_error)

    return get_module(path, start_adress)

    

def import_lib(file_name:str, start_adress:int, no_error:bool=False) -> ModuleInfo:
    """Import a module from the library. Path is :
    Linux: /usr/lib/Smart-SmartyKit/global_lib/...
    Windows: %LOCAL_APPDATA%/Smart-SmartyKit/lib/global_lib/"""

    control_lib()

    path = os.path.join(PATH_LIB["global"], file_name)

    if not Path(path).is_file():
        raise ModuleError(f"File '{path}' not exist!", no_error=no_error)

    return get_module(path, start_adress)

def import_smart(file_name:str, start_adress:int, no_error:bool=False) -> ModuleInfo:
    """Import a module from the smart library. Path is :
    Linux: /usr/lib/Smart-SmartyKit/smart_lib/...
    Windows: %LOCAL_APPDATA%/Smart-SmartyKit/lib/smart_lib/"""

    control_lib()

    path = os.path.join(PATH_LIB["smart"], file_name)

    if not Path(path).is_file():
        raise ModuleError(f"File '{path}' not exist!", no_error=no_error)

    return get_module(path, start_adress)

def import_all(file_name:str, start_adress:int) -> ModuleInfo:
    """Import a module from all the path (file, lib, smart).
    The order is file, lib, smart."""
    try:
        return import_module(file_name, start_adress, no_error=True)
    except ModuleError:
        pass

    try:
        return import_lib(file_name, start_adress, no_error=True)
    except ModuleError:
        pass

    try:
        return import_smart(file_name, start_adress, no_error=True)
    except ModuleError:
        raise ModuleError(f"Module '{file_name}' not found in any path.")