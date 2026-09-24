# To Do

The future features of Smart, or fix bugs.

If the task is a fix, the text is _italic_.

If the task is an important feature, the text is **bold**.

The task with `?` is a task that is not sure if it will be implemented.

If the task is a bug you can also add an issue on GitHub.

## Tasks

- _Fix: small bug on windows: the path of the library is not joined correctly: ...lib\global_lib\screen_tool/screen_tool.sma_
- Add operator: `^`... Add comparator: `and` `or` `>` `<=`
- Make the libraries for Smart: `math` ?, `string`, library for write in RAM/ROM ?
- **Add string and list with size variable ?**
- Add class object for Smart ?
- For Smart system variable, use 0 page mode
- Add for variable: `.x += ...`.
- Add on increment/decrement on advenced value the index on runtime value: `.x = 1;~str="";~str[.x]++;`
- Better threading: fix some problems with no shared stack + add some tests
- On thread, add swith when a print beetween all character + add a swith on the input (the loop of input)
- On math, add parentheses `(1+2)*3`
- On the library input, add new features: set a readline with print character, add a clear string (clear the string when the end is `\r` for exemple) on end mode...
- On string library, add count, replace, in...
- Add new test with using timeout: while True test... And add option for when the time is out, the output is given and test if the output is correct.
- Set a refactor for build-in function: add all build-in at class SmartBuiltin, and maybe add a better control of argument. Maybe set a new module. And finally, refactore the class SmartBuiltin: this class is for a function, and on a module, set the instances of this class?
- Fix: on function with parameter, it is impossible to give a list (because parameter is split with `,`)
- Fix: on the test "Test library import", error with adresse counter.
- Add new auto test: set some test with thread on modules
- Add test for lib:
    - Add test for assembly lib
    - Add test for dynamic_run **need a refactor on emulator for run this lib**
    - Add test for memory lib **need to have dynamic_run ok on emulator**