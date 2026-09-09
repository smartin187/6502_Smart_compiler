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
