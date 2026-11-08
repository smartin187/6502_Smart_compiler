# string library

This library is for string and character manipulation.

## Sub modules

### `string.sma`

_The main module._

For import module:

```Smart
import "string/string.sma";
```

#### `count: ~string, .char`

Return the number of occurrences of the character `.char` (or other simple value) in the string or list `~string`.

```Smart
import "string/string.sma";

~my_string = "AAABBBB";

.count_a = count: ~my_string, 'A';
.count_b = count: ~my_string, 'B';

// show the count as ASCII character:
print: .count_a + '0';
print: .count_b + '0';
```

#### `in: ~string, .char`

Return `True` (1) if the character is in the string or list, else return `False` (0).

```Smart
import "string/string.sma";

~my_string = "ABCD";

.in_result = in: ~my_string, 'A';
print: .in_result + '0';

.in_result = in: ~my_string, '1';
print: .in_result + '0';

.in_result = in: ~my_string, 0; // True because 0 is on the string
print: .in_result + '0';
```

#### `str_len: ~string`

Return the length of the string or list. On Smart, all string or list have a lenght of 21, so this function return the last index of the advenced value how is not a null byte (0). If the string is empty, return 0.

```Smart
import "string/string.sma";

~my_string = "ABCD";
.len = str_len: ~my_string;
print: .len + '0'; // 4

~my_string[-1] = 'A'; // the last index is not null byte
.len = str_len: ~my_string; // 21
print: .len + '0'; // print E because 21 + ASCII 0
```

### `convert.sma`

This module is for conversion between the ASCII code of a character and its integer value.

For import:
```Smart
import "string/convert.sma";
```

#### `int_to_char: .int`

This function returns the ASCII character of the integer passed as argument.

#### `char_to_int: .char`

This function returns the integer value of the ASCII character representation passed as argument.
