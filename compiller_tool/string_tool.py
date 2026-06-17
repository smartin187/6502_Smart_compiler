# -*- coding: utf-8 -*-

"""
This module have function for operation with string.
Function:
- split_code
- replace_code
- in_code
- good_variable_name
- EscapeChar

Constent:
- SMART_KEYWORD (dict)
"""
import logging
from compiller_tool.color_tool import Colors
from compiller_tool.smart_exception import SmartError

class EscapeChar:
    """The escape char for str and char value."""
    ESCAPE_CHAR = {"\\r":"\r", "\\\"":"\"", "\\'":"'"}        # the escape characters for str and char (\r...)
    DOUBLE_SLASH = "\\\\"
    PLACE_HOLDER_SLASH = "`smart_double_slash"                  # set ` because this character is not used in str / char value.



def split_code(
        code:str,
        sep:str | tuple[str, ...]=(" ",),
        string:tuple[tuple[str, str]]=(("'", "'"), ('"', '"'), ("[", "]")),
        max_split:int=0
    ) -> list[str]:
    """Split a code, but ignore sep if it is in a str or char Smart Value.
    arg max for set the max split. If max=0, no limit of split."""
    def char_is_sep(i:int) -> bool | str:
        """Return the sep if char is in sep, False else."""
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
            if char == open_str and last_char != "\\":
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
        string: tuple[tuple[str, str]] = (("'", "'"), ('"', '"'), ("[", "]")),
        max_replace: int = -1
    ) -> str:
    """Replace a substring in code, but ignore if it is in a str or char Smart Value.
    arg count for set the max replacements. If count=-1, no limit of replacements."""

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
        string: tuple[tuple[str, str]] = (("'", "'"), ('"', '"'), ("[", "]"))
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

counter_adress_value = 0        # the relative adress used by set_one_A_value. Be carful with this value.

SMART_KEYWORD = ("void", "if", "elif", "else", "while", "break", "continue")

def good_variable_name(name:str) -> bool:
        """Return True if the name of variable is good, False else.
        An variable name can have :
        - Any letter lower (a-z). Special letter (éèëù...) are accepted.
        - Any number 0-9
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
    """Return a list of int, the ascii code of char on the string, if the char is \r, \", \', the element of list have it."""        
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


def get_bloc(line_conter:int, code:str, error_message:str="") -> str:
    """Return the content of bloc {}
    
    error_message is the text for info about error."""
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
    """Return the int value of adress from a str. The str adress is in hex and in little endian (example: 00 04 for 0x0400)"""
    string = string.replace(" ", "")
    if len(string) != 4:
        raise ValueError(f"Adress str must have 4 char, not {len(string)} char.")
    
    return int(string[2:4] + string[0:2], 16)