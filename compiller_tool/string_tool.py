# -*- coding: utf-8 -*-

"""
This module have function for operation with string.
Function:
- split_code
- replace_code
- in_code
"""


def split_code(
        code:str,
        sep:str | tuple[str, ...]=(" ",),
        string:tuple=("'", '"'),
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
            if char in string:
                on_str = True
                open_str = char

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
        string: tuple = ("'", '"'),
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
            if char in string:
                on_str = True
                open_str = char
                result.append(char)
                i += 1
            elif code[i:i+len(old)] == old:
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
        string: tuple = ("'", '"')
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
            if char in string:
                on_str = True
                open_str = char
                i += 1
            elif code[i:i+len(substring)] == substring:
                return True
            else:
                i += 1
        else:
            if char == open_str:
                on_str = False
            
            i += 1
    
    return False

counter_adress_value = 0        # the relative adress used by set_one_A_value. Be carful with this value.