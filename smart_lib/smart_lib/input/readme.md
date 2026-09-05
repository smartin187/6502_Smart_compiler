# input lib

This library is for the input with keyword of Apple1/SmartyKit.

## Modules

### `readkeys.sma`

This module have the function `readkeys`. This function is for get a string from the keyboard.

This function take 2 arguments:
- The string where the input will be stored.
- A simple value, can be `False` or `0` for no character of end, or a character to stop the input (you can set `\r`).

**Usage:**


```Smart
import "input/readkeys.sma";

~my_string = "";

// read 21 character (len of string):
readkeys: ~my_string, False;  // on ~my_string will be the input from keyword.

print: ~my_string;


// read while the caracter is not '\r' or 21 was read:
readkeys: ~my_string, '\r';
print: ~my_string;

```

**Note**: the end character is not removed from the string. So if the end is `\r`, you can have a `\r` at the end of the string, or not if the user press 21 character.

> Carful if you set a character to stop reading. If they are character on string before the readkeys, the character don't be removed when the stop. For exemple:

```Smart
import "input/readkeys.sma";

~my_string = "THIS TEXT DONT REMOVE";
readkeys: ~my_string, '\r';
print: ~my_string; // if you press \r before the 21, you see the end of the string.
```

For exemple, if you press enter at 5 character, you will see you 5 character and `TEXT DONT REMOVE`
