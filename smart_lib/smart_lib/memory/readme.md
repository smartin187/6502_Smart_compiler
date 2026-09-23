# Memory library

This library is for use the memory.

> **Warning**: the Smart emulator is not compatible with this library...

## Features

### Module `memory.sma`

Import the module:

```smart
import "memory/memory.sma";
```

Next you can use the functions:

```smart
import "memory/memory.sma";
.value = read_simple: 0x00, 0x00; // read the value at the address 0x0000

print: .value;
```

> The address are in big-endian format.
