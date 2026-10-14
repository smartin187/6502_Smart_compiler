# Assembly lib

This library is for get the assembly operation on the Smart programme.

## Features

Import the library:

```smart
import "assembly/simple_operation.sma";
```

_Actually, the library is only for 1 byte operation._

Next you can run assembly operation:

### 1 byte operation

This operation are on 1 byte, without value or address after. For exemple `NOP`, `INX` (increment X)...

```smart
import "assembly/simple_operation.sma";
NOP;
INX;
ROR;
```

You will get: `0400: EA E8 6A 00` (the last `00` is the end of programme, but the other opcode are the assembly operation you run).

> **Warning**: some operation are not compatible with the Smart emulator... Use a real emulator of run on SmartyKit/Apple 1.
