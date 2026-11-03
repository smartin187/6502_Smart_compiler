# Random

This library is for get random value (0 to 255). They are different function for different random mode.

## Features

### Module `random.sma`

First import the module:

```Smart
import "random/random.sma";
```

Next you can use the functions:

#### Function `random_sum`

This function do the sum of the value of regester A, X, Y and the stack pointer.

The advantage is the value of regester and stack change regularly, the value can be random. But the disadvantage is the value can be the same if the program before the call set a defined value for all registers and stack pointer.

```Smart
import "random/random.sma";

.random_value = random_sum:;

print: .random_value;
```

#### Function `random_sub`

This function is the same as `random_sum` but it do the substraction of the value. They are the same advantage and disadvantage. But you can mix the function on your program for get a better random value.

```Smart
import "random/random.sma";

.random_value = random_sub:;
print: .random_value;
```

#### Function `random_press`

This function need to the user press a key during the call.

When the function is call, a loop increment a value (on modulo 256). When the user press a key, the function break the loop and return the value. The [loop is very fast](#time-of-a-loop) so the user can't know the current value. The advantage is the value is very random and can't be predicted, but the disadvantage is the user need to press a key.

```Smart
import "random/random.sma";

print: "PRESS A KEY";
.random_value = random_press:;
print: .random_value;
```

##### Time of a loop

On the loop, they are 3 instruction:
- INX (2)
- LDA absolute (4)
- BPL (3 if not branch)

So a loop take 9 cycles. The processor speed is 1MHz, so a loop take 9 microseconds. This value is very random, because the user can't predict the time of a loop. The user can press a key at any time, so the value is very random.
