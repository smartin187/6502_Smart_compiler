# Smart Compiler

![Logo](./img/logo_smart_small.png)

Smart Compiler is a project that aims to make programming on a Smarty Kit (an Apple-1 replica) simpler.

This repository contains a compiler for Smart code (a language created for the Smarty Kit) and an interpreter for that language (if you want to test a program without a Smarty Kit).

>Smart is in development. Some bugs are to fix. Report issues if you have problems. New features will be added soon...

## The Smart programming language

Smart is a very simple programming language. If you need more features, you should use BASIC instead, or write assembly directly.

_New features will be added soon..._

The advantage of Smart is that it is optimized for the Smarty Kit CPU.

Once your program is ready, you can either [compile it](#compile-smart-code) or [run it in the interpreter](#interpret-smart-code-emulator).

### Writing Smart code

Below is the complete list of Smart features and syntax.

#### Generic syntax

Smart instructions must be separated by semicolons `;`. Newlines and spaces can be added anywhere in your code.

##### Comments

Smart comments use two slashes: `//`. Everything that follows on the same line is ignored.

#### Value types

There are currently two value types: a hexadecimal value and a char (a single character).

_Simple value (on 1 byte):_

##### `bool` value

Can be `True` or `False` (upper case in first character).

##### `hex` value

This value is a 1-byte hexadecimal number, ranging from `00` to `FF`.

**You need to set `0x` before:**
- `0x00`
- `0x41`

##### `int` value

This value is beetween 0 and 255.


##### `char` value

This value is a 1-byte character. Here is the list of allowed characters:

`!"#$%'()*,+-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`

The character must be wrapped in single quotes.

Examples:
- `'A'`
- `'B'`
- `'1'`

---

_advanced value (on 21 bytes):_

##### `str` (string of `char`) and `list`

This value is saved on 21 bytes, so the max length of a `str` of `list` is 21 characters.

###### `str` value

It starts and ends with double quotes.

Allowed characters are the same as for [`char`](#char-value).

> **Only on print function**, the `str` can be longer than 21 **if the string is know at the compile time!**. For other `str`, the max length is 21.

**Escape caracters**

One `str`, you have escape caracters.

- `\r`: carring return
- `\"`: for have a `"`

###### F-string

F-string is a mode for add simple value incide a `str` value.

F-string start with `F` and have `{}` for add a simple value.

`F"TEXT{SIMPLE_VALUE}TEXT"`

###### `list` value

`list` value is an other representation of `str` value.

`list` start with `[` and end with `]`. Inside, you can add simple value separated by `,`.

`[SIMPLE_VALUE,SIMPLE_VALUE]//max len of 21`

###### Index on `list` or `str`

See the documentation of [advanced variable](#indexing-on-advanced-variable-list-or-str) for indexing on `list` or `str` value.


#### Using registers

In Smart, you can directly modify the value of an accumulator register.

However, it is not recommended, because registers are used for many operations (your value may get overwritten...)

The three available accumulators are A, X, and Y.

To assign a value, use the syntax `RegisterName = Value`:
```Smart
A = 0x00;  // put the hex value into A
A = 'B'; // put the character B into A
```

Registers X and Y are rarely used directly, because they are normally used for loops...

#### Variables

On Smart, they are 2 variables type: simple and advenced.

Simple variable can be used for [`bool` value](#bool-value), [`hex` value](#hex-value), [`int` value](#int-value), and [`char` value](#char-value).

Advenced value can be used for [`str` value](#str-string-of-char).

>Carful: advenced value need a lot of memory!

##### Simple variable

Simple variables must start with a dot `.`.


###### Syntax

The syntax is `.variable_name = value;`.

Variable names can contain lowercase letters, digits, and underscores `_`. A leading dot `.` is required, but dots cannot appear elsewhere in the name.

To use the value of a variable (for example, in a function), write the variable name (including the leading dot).

##### Advenced variable

The syntax is `~variable_name = "VALUE";`.

Variable names can contain lowercase letters, digits, and underscores `_`. A leading tilde `~` is required, but dots cannot appear elsewhere in the name.

To use the value of a variable (for example, in a function), write the variable name (including the leading tilde).

>Carful: advenced variable canno't be used for some operation (like math operation...).

###### Indexing on advanced variable (`list` or `str`)

For get a value from an index on advanced variable (`list` or `str`), use: `~var[index]`.

Index need to be a value between `0` and `20`, or `-21` and `-1` (for reverse index).

You can set a variable for the index, but the index can't be negative. If you need a negative index, you can do: `~var[21-.my_variable]` (because the length of `list` or `str` is 21).

You can also change value of an index on advanced variable:
```Smart
~var[index] = 'A';
```


#### Labels (anchors)

You can create labels (anchors) and later use the [`goto`](#goto) function to jump to a label.

##### Syntax

The syntax is: `#label_name;`.

You can then use [`goto`](#goto).

#### Operator

Operator are the mathematic operator and logic operator.

For all operator, all value are accepted. If the value is a char, the value used is the ASCII code.

**Warning**: `str` value are not accepted, except for `==` operator.

##### `+`

Add tow value.

>Note: if the result exceeds 255, the carry flag is set to 1.

##### `-`

Substract tow values.

##### `*`

Multiply tow values

##### `/`

Division integer of 2 values. The result is round for a integer result.

**Warning:** division by zero; do an infinite loop!

##### `==` (equality)

Compare 2 value, return True if value are equal False else.

>This value can be `str`. If it is the case, the `str` can't be compared to an other value type.

##### Example

```Smart
.x = 1 + 1;

.y = 10 == 10;

.z = 'A' == 65
```

#### Condition

You can use a conditionnal bloc with `if`.

```Smart
if condition{;
    // code
}
```

The condition is a value (int, char, boolean value...). If the value is not `0`, the bloc is run.

Then an `if` bloc, you can set a `elif` bloc. This condition is verifed if the condition of `if` bloc is `False`.

```Smart
if False{;
    print: "IF CODE";
}
elif True{;
    print: "ELIF CODE";
}
```

>You can have several `elif` bloc.

Then an `if` or `elif` bloc, you can set a `else` bloc:

```Smart
if False{;
    print: "IF CODE";
}
else{;
    print: "ELSE CODE";
}
```

##### Exemple

```Smart
if True == True{;
    print: "THE CONDITION IS TRUE";
}
```

#### Loop

You can do loop in Smart.

Smart have the [`while` loop](#while-loop).

>Moreover, you can build your own loop with [goto](#goto) and [label](#labels-anchors).

>Note: you can also set a infinit loop with recursive function. It work, the perf are low...

On loop, you can use [`break`](#break) and [`continue`](#continue) keyword.

##### `while` loop

This loop is runing as long as the condition is `True`.

If you set `True` on the condition, you have an infinity loop.

###### Sintaxe

```Smart
while True{;
    print: "INFINIT LOOP";
}
// you can set any condition:
.my_variable = 1;
while 1 == .my_variable{;
    // ...
}
```

##### `break`

Use this keyword for go out of loop.

###### Sintaxe

```Smart
while True{;
    print: 'A';
    break;  // go out of loop.
    print: "THIS CODE WILL NOT RUN";
}
```

##### `continue`

Use this keyword for restart the loop.

###### Sintaxe

```Smart
while True{;
    print: 'A';
    continue;  // restart the loop
    // the code after will not run

}
```

#### Functions

Smart provides several built-in functions. You can build your own function.

The call syntax is: `functionname: argument;`.

Some functions do not take any arguments, but you still need to include the colon `:`.

They are return-function and function. If the function is a return-function, you can do:
```Smart
.variable = function_name:;
```

##### Smart built-in functions

###### `print`

This function prints a character to the screen.

The value can be a `char`. It can also be a `hex` or `int` (in which case the ASCII code is used), and you can also use a `str`.

**Example**

```Smart
print: 0x41;  // using hex, 0x41=65 (ASCII code for A)
print: '1'; // using a char
print: "HELLO WORLD";   // using a str

.my_variable = 0x42;
print: .my_variable; // B
print: 0x42 + 1;  // C
```

###### `input`

This function is a return-function. This function return a char value of pressed key.

Example:
```Smart
.key = input:;

print: .key
```

###### `goto`

This function jumps to a [label](#labels-anchors).

First define a label, then use this function to jump back to it.

Pass the label name as the argument.

This feature is mainly used to create loops.

**Example**

```Smart
#loop;

print: "INFINITE_LOOP!";

goto: loop;
```

###### `asm_entry`

Use this functtion for enter assembly code for MOS 6502.

**Warning:** if you use the [Smart Emulator](#interpret-smart-code-emulator), `asm_entry` can cause errors...

Exemple:
```Smart
asm_entry: "A9 41 20 EF FF";    // display A on monitor
```

###### `wozm` (Woz Monitor)

This function stop programme and return to Woz Monitor.

This function go to `FF1F`, the Woz Monitor `GETLINE`.

Not take any argument.

###### `quit`

This function exits the program.

It does not take any arguments.

> `quit` stop the programme but not return to Woz Monitor. Use `wozm` if you want to return to Woz Monitor.

##### Build your own function

You can build your own function.

The syntaxe is:
```Smart
void name_of_function{;
    // function code
}
```

For use your function:
```Smart
name_of_function:;
```

You can do a recursive function. Smart use the stack for the recursive function. You can have a max recursive of 128 (`256/2`).

> If you exced the max recursive of 128, you will have stack overflow and the program can crash.

If your function is a return-function, you need the line:
```Smart
void returnfonction{;
    // code of function
    return 1;
}
```

> **Carfull**: some bug are to fix with return function !

#### Runtime error

You can set a runtime error with keyword `error`. Next keyword you set a error code (can be `char`, `hex`, `int`).

```Smart
error 'A'; // the error code is 'A'
```

If an runtime error is set, the program displays `E` and next the error code.

>**The error code is display as ASCII code.** If your error code is `65` the error code is `A`.

>Warning: if the ASCII code can't be display by SmartyKit, the runtime error print only `E`.

>Note: the value of `error` keyword can be a `bool`, but the character of `0` and `1` ASCII are not visible...

The program is stopped when a runtime error is set.

>If you use runtime error, you can say what is your error code. For example: error `A` is "invalid value", error `B` is ...

##### Runtime error built-in

They are built-in runtime error for some operation:
- error `'/'`: division by zero
- error `'I'`: index out of range (for advanced variables)

_Please do not use this error code for your runtime error: you can't know what error is it..._

## Compile Smart code

Once you have your code, the first option is to compile it so it can run on a Smarty Kit (code is theoretically compatible with an Apple 1).

To do so, download this repository and run:

`python3 main.py your_file.sma`

_Smart code typically uses the `*.sma` extension._

The compilation result is printed in the terminal, and it is also written to a file with the `*.asm` extension. In this example, the generated file is `your_file.asm`.

To use this code on the Smarty Kit, you can copy/paste it into the Woz Monitor (type `0400:` first if you want to start at address `0x0400`; otherwise, use a different address).

To run the program, type `0400R` in the Woz Monitor (assuming `0400` is the program address).

If your program is long, you can also use the [Smart interpreter](#interpret-smart-code-emulator) on your computer so you don't have to copy it by hand. The interpreter is also useful for debugging, or when your program is slow to execute.

## Interpret Smart code (emulator)

If your program is long to type in, or if you don't have a Smarty Kit, you can use the Smart interpreter.

Note that another option is to use a real Apple-1 emulator to get the exact same behavior.

The Smart interpreter lets you execute Smart code directly on your computer.

Download the code, then run in a terminal:

`python3 smart_emulator.py your_program.sma`

A window opens with the interpreter. Your code will run as if it were on a Smarty Kit.

### Debugging with the interpreter

You can also use the interpreter to debug your program. It allows you to inspect RAM contents as well as the accumulator state and the carry flag.

In the interpreter window, click `see memory` to view memory in real time.

### Speeding up program execution

On a Smarty Kit, execution speed is slow. With the interpreter, you can increase the speed: click `setting`, then uncheck `run with speed of 1Mhz`. Execution will become much faster.


## Information about memory

Smart use RAM.
- `0x0300` to `0x0400`: variables
- `0x0000` to `0x02FF`: Smart system:
>`0x0000`: save of A (for return-function)<br>`0x0001`: value of return-function<br>`0x0002`: `01` if need to call `else bloc` (after `if`). If `0x02E9 = 01` bloc `else` or `elif` are called.<br>`0x0003`: used for math (for operator `*` and `/`).<br>`0x0004` to `0x0032`: used for string `str`.

## VS Code extension

An extention for VS Code set a coloration for Smart language.

Go to the reposytory: [smart_smartykit_vscode_extension-cpmpr](https://github.com/smartin187/smart_smartykit_vscode_extension-cpmpr).


