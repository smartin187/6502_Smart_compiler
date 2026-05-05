# Smarty Compiler

Smarty Compiler is a project that aims to make programming on a Smarty Kit (an Apple-1 replica) simpler.

This repository contains a compiler for Smart code (a language created for the Smarty Kit) and an interpreter for that language (if you want to test a program without a Smarty Kit).

## The Smart programming language

Smart is a very simple programming language. If you need more features, you should use BASIC instead, or write assembly directly.

_New features (especially math operations) will be added soon..._

The advantage of Smart is that it is optimized for the Smarty Kit CPU.

Once your program is ready, you can either [compile it](#compile-smart-code) or [run it in the interpreter](#interpret-smart-code-emulator).

### Writing Smart code

Below is the complete list of Smart features and syntax.

#### Generic syntax

Smart instructions must be separated by semicolons `;`. Newlines and spaces can be added anywhere in your code.

##### Comments

Smart comments use two slashes: `//`. Everything that follows on the same line is ignored.

#### Value types

There are currently two value types: a hexadecimal value and a char (a single character). There is also a third type that can only be used in the [print](#print) function: a string of characters (`str`).

##### `hex` value

This value is a 1-byte hexadecimal number, ranging from `00` to `FF`.

##### `char` value

This value is a 1-byte character. Here is the list of allowed characters:

`!"#$%'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`

The character must be wrapped in single quotes.

Examples:
- `'A'`
- `'B'`
- `'1'`

##### `str` (string of `char`)

This value cannot be stored in a variable or in a register because it requires multiple bytes. However, you can use it in the [print](#print) function.

It starts and ends with double quotes. There is no length limit.

Allowed characters are the same as for [`char`](#char-value).

#### Using registers

In Smart, you can directly modify the value of an accumulator register.

However, it is not recommended, because registers are used for many operations (your value may get overwritten...)

The three available accumulators are A, X, and Y.

To assign a value, use the syntax `RegisterName = Value`:
```Smart
A = 00;  // put the hex value into A
A = 'B'; // put the character B into A
```

Registers X and Y are rarely used directly, because they are normally used for loops...

#### Variables

Smart variables must start with a dot `.`.

Values that can be stored in a variable are [`hex`](#hex-value) and [`char`](#char-value).

The maximum number of variables is 256 (size of Smart's virtual RAM).

##### Syntax

The syntax is `.variable_name = value;`.

Variable names can contain lowercase letters, digits, and underscores `_`. A leading dot is required, but dots cannot appear elsewhere in the name.

To use the value of a variable (for example, in a function), write the variable name (including the leading dot).

#### Labels (anchors)

You can create labels (anchors) and later use the [`goto`](#goto) function to jump to a label.

##### Syntax

The syntax is: `#label_name;`.

You can then use [`goto`](#goto).

#### Math operations

Currently, only addition is available.

Note: if the result exceeds 255, the carry flag is set to 1.

##### Example

```Smart
.result = 01 + 01;    // value 02 in result
.result2 = 05 + 1F;   // value 36 (0x24) in result2
```

You can also use a `char`; in that case, the character's ASCII code is added:
```Smart
.result = 'A' + 01;   // value 0x42 in result
```

#### Functions

Smart provides several built-in functions. You can build your own function.

The call syntax is: `functionname: argument;`.

Some functions do not take any arguments, but you still need to include the colon `:`.

##### Smart built-in functions

###### `print`

This function prints a character to the screen.

The value can be a `char`. It can also be a `hex` (in which case the ASCII code is used), and you can also use a `str`.

**Example**

```Smart
print: 41;  // using hex, 0x41=65 (ASCII code for A)
print: '1'; // using a char
print: "HELLO WORLD";   // using a str

.my_variable = 42;
print: .my_variable; // B
print: 42 + 01;  // C
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

###### `quit`

This function exits the program.

It does not take any arguments.

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
