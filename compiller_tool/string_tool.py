# -*- coding: utf-8 -*-

"""
This module has functions for operations with strings.
Function:
- split_code
- replace_code
- in_code
- good_variable_name
- EscapeChar

Content:
- SMART_KEYWORD (dict)
"""
import logging
from compiller_tool.color_tool import Colors
from compiller_tool.smart_exception import SmartError
from compiller_tool.compiller_data_run import EscapeChar

def split_code(
        code:str,
        sep:str | tuple[str, ...]=(" ",),
        string:tuple[tuple[str, str], ...]=(("'", "'"), ('"', '"'), ("[", "]")),
        max_split:int=0
    ) -> list[str]:
    """Split code, but ignore sep if it is in a str or char Smart Value.
    The arg max sets the max split. If max=0, there is no limit to the split."""
    def char_is_sep(i:int) -> bool | str:
        """Return the sep if char is in sep, False otherwise."""
        for s in sep:
            if code[i:i+len(s)] == s:
                return s
        return False



    if code == "":
        return []

    on_str = False
    open_str = ""

    if isinstance(sep, str):
        sep = (sep,)

    split = []

    new_element = []

    nb_split = 0

    wait_char = 0

    last_char = ""

    for i, char in enumerate(code):
        if wait_char:
            wait_char -= 1
            continue

        if not on_str:
            for open_quote, close_quote in string:
                if char == open_quote:
                    on_str = True
                    open_str = close_quote
                    break

            char_is_sep_result = char_is_sep(i)

            if char_is_sep_result:
                wait_char = len(char_is_sep_result) - 1

                if max_split:
                    if nb_split == max_split:
                        new_element.append(char)
                        continue
                    else:
                        nb_split += 1
                split.append("".join(new_element))
                del new_element[:]

            else:
                new_element.append(char)


        else:
            if char == open_str:

                before_close = code[0:i]

                counter = 0

                for _char in reversed(before_close):
                    if _char == "\\":
                        counter += 1
                    else:
                        break

                if counter % 2 == 0:
                    on_str = False

            new_element.append(char)

            last_char = char

    if new_element != []:
        split.append("".join(new_element))

    return split


def replace_code(
        code: str,
        old: str,
        new: str,
        string: tuple[tuple[str, str], ...] = (("'", "'"), ('"', '"'), ("[", "]")),
        max_replace: int = -1
    ) -> str:
    """Replace a substring in code, but ignore if it is in a str or char Smart Value.
    The arg count sets the max replacements. If count=-1, there is no limit to the replacements."""

    if code == "" or old == "":
        return code

    on_str = False
    open_str = ""
    result = []
    i = 0
    replacements = 0

    while i < len(code):
        char = code[i]

        if not on_str:
            for open_quote, close_quote in string:
                if char == open_quote:
                    on_str = True
                    open_str = close_quote
                    result.append(char)
                    i += 1
                    break
            else:
                if code[i:i+len(old)] == old:
                    if max_replace == -1 or replacements < max_replace:
                        result.append(new)
                        i += len(old)
                        replacements += 1
                    else:
                        result.append(char)
                        i += 1
                else:
                    result.append(char)
                    i += 1
        else:
            if char == open_str:
                on_str = False

            result.append(char)
            i += 1

    return "".join(result)


def in_code(
        substring: str,
        code: str,
        string: tuple[tuple[str, str], ...] = (("'", "'"), ('"', '"'), ("[", "]"))
    ) -> bool:
    """Check if substring is in code, but ignore if it is in a str or char Smart Value.
    Similar to 'substring in code', but with string awareness.
    Returns True if substring is found outside strings, False otherwise."""

    if code == "" or substring == "":
        return False

    on_str = False
    open_str = ""
    i = 0

    while i < len(code):
        char = code[i]

        if not on_str:
            for open_quote, close_quote in string:
                if char == open_quote:
                    on_str = True
                    open_str = close_quote
                    i += 1
                    break
            else:
                if code[i:i+len(substring)] == substring:
                    return True
                i += 1
        else:
            if char == open_str:
                on_str = False

            i += 1

    return False

counter_adress_value = 0        # the relative address used by set_one_A_value. Be careful with this value.

SMART_KEYWORD = ("void", "if", "elif", "else", "while", "break", "continue", "error", "for", "compiletime", "import")

def good_variable_name(name:str) -> bool:
        """Return True if the name of the variable is good, False otherwise.
        A variable name can have:
        - Any lowercase letter (a-z). Special letters (éèëù...) are accepted.
        - Any digit 0-9
        - underscore _"""

        if name in SMART_KEYWORD:
            logging.error(f"{Colors.RED}Name `{name}` is a Smart keyword, can't be used for a name.{Colors.RESET}")   # set a error message, but SmartException is used on the call of function
            return False

        if name[0].isdigit():
            return False

        for char in name:
            if (not (char.isalpha() or char.isdigit() or char == "_")) or char.isupper():
                return False
        return True

def get_char_from_str(string:str) -> list[str]:
    """Return a list of the characters of the string. If the char is \r, \", \', the element of the list has the escaped form."""
    result = []

    counter = 0

    while counter != len(string):
        char = string[counter]


        if char == "'":
            result.append("\\'")

        elif char == "\"":
            result.append('\\"')

        else:
            result.append(char)

        counter += 1

    return result


def get_bloc(line_conter:int, code:list[str], error_message:str="") -> tuple[str, int]:
    """Return the content of block {}

    error_message is the text used for info about the error."""
    # get the code of function:

    funciton_line = line_conter + 1

    func_code = ""

    number_open = 1

    try:
        while True:
            code_line_func = code[funciton_line]
            close_pos = None

            for i, ch in enumerate(code_line_func):
                if ch == "{":
                    number_open += 1
                elif ch == "}":
                    number_open -= 1
                    if number_open == 0:
                        close_pos = i
                        break

            if close_pos is not None:
                inside = code_line_func[:close_pos]
                if inside.replace(" ", "") != "":
                    func_code += inside + ";"

                code[funciton_line] = code_line_func[close_pos + 1:]
                break

            func_code += code_line_func + ";"
            funciton_line += 1


    except IndexError:
        raise SmartError(error_message + ", brackets '{' was never closed.", line_conter)

    return func_code, funciton_line

def get_int_adress_from_str(string:str) -> int:
    """Return the int value of the address from a str. The str address is in hex and in little endian (example: 00 04 for 0x0400)"""
    string = string.replace(" ", "")
    if len(string) != 4:
        raise ValueError(f"Adress str must have 4 char, not {len(string)} char.")

    return int(string[2:4] + string[0:2], 16)

def get_hex_from_int(value:int) -> str:
    """Return the hex value of int, on 2 characters (1 byte)."""
    hex_value = hex(value)[2:].upper().zfill(2)

    return hex_value


def adress_for_RAM(adress:int) -> str:
    """Return the RAM address in hex.
    Example:
    768 -> 00 03"""
    adress_RAM = hex(adress)[2:].upper()

    adress_RAM = "0" * (4 - len(adress_RAM)) + adress_RAM

    adress_RAM = adress_RAM[2:] + " " + adress_RAM[:2]
    return adress_RAM

def get_str(string:str, line_conter:int=0) -> str:
    """Return the str value. Add the escape char."""

    string = string.strip()

    if not string.startswith('"'):  # error if the function was called on a value other than a str
        raise SmartError(f"Value '{string}' is not a str value.", line_conter)


    str_value = ""
    escape_char = False
    end = False

    for char in string[1:]:
        if end: # a char is after the " for close
            raise SmartError(f"Invalid syntax after str value: '{string}'", line_conter)

        if char == '"' and not escape_char:
            end = True
            continue

        str_value += char

        if char == "\\":
            escape_char = not escape_char

        else:
            escape_char = False

    # replace char:

    str_value = str_value.replace(EscapeChar.DOUBLE_SLASH, EscapeChar.PLACE_HOLDER_SLASH)   # use a placeholder for double slash

    for char in EscapeChar.ESCAPE_CHAR:
        replace = EscapeChar.ESCAPE_CHAR[char]

        str_value = str_value.replace(char, replace)

    str_value = str_value.replace(EscapeChar.PLACE_HOLDER_SLASH, "\\")


    if len(str_value) == 0:
        logging.warning("str value is empty!")
    elif len(str_value) == 1:
        logging.warning("str value have a len of 1. Please use a char value.")

    return str_value

def get_char(char_type:str) -> str:
    """Return the char value of Smart."""
    def char_error() -> None:
        """Raise SmartError if the char value doesn't have exactly 1 character."""
        raise SmartError(f"The char value `{char_type}` don't have 1 character.")

    if char_type.startswith("'") and char_type.endswith("'"):
        char = char_type[1:-1]

        if len(char) == 2 and char == "\\\\":
            code_ascii = ord("\\")

        elif len(char) == 2 and char.startswith("\\"):
            if char in EscapeChar.ESCAPE_CHAR:
                code_ascii = ord(EscapeChar.ESCAPE_CHAR[char])
            else:
                char_error()

        elif len(char) == 1:
            if char.islower():
                raise SmartError("char cannot be lower.")

            if char == "'":
                raise SmartError(f"Error with char value `{char_type}`.")

            code_ascii = ord(char)

        else:
            char_error()

        code_hex = hex(code_ascii)[2:]
        code_hex = code_hex.upper()
        return code_hex

    else:
        raise SmartError(f"The char value (`{char_type}`) was never closed.")

def good_hex(code:str) -> bool:
    """Return True if the hex value is good, False else."""
    try:
        int(code, base=16)
    except:
        return False
    else:
        return True if len(code) == 2 else False

def control_hex(code:str) -> None:
    """If good_hex returns False, raise SmartError."""
    if not good_hex(code):
        raise SmartError(f"Bad hex value '{code}'")

