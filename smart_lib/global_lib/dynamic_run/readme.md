# Dynamic run library

This library run a programme in op codes on a advenced value at runtime.

> **Warning**: this library is not compatible with the Smart Emulator.

## Features

Import the library:

```smart
import "dynamic_run/dynamic_run.sma";
```

Use the function `dynamic_run` to run a programme on a advenced value:

```smart
import "dynamic_run/dynamic_run.sma";

// the programme:
~code = [0xA9, 0x41, 0x20, 0xEF, 0xFF, 0x60];
dynamic_run: ~code;
```

This programme load on A `0x41`, and call `echo` of Woz Monitor.

**Warning**: if your programme is less than 21 bytes, **you must** add `0x60` at the end of your programme. If the programme have a lenght of 21 bytes (the maximum for adcenved value), you don't need to add `0x60` at the end of your programme.


