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
- Add new test with using timeout: while True test... And add option for when the time is out, the output is given and test if the output is correct
- Fix a problem: if a `for` loop on function on module, error: the variable of for (`.i`) have a error "variable already exist".
- Set a refactor for build-in function: add all build-in at class SmartBuiltin, and maybe add a better control of argument. Maybe set a new module. And finally, refactore the class SmartBuiltin: this class is for a function, and on a module, set the instances of this class?
- Fix the probleme with the progress bar: the progress bar is set to 0 the time of compile a bloc (`if`, `else`...). Set only the main call of compile_smart can edite the value of progresse bar + remove the log "Build completed" and "Memory info" for the block of code, only for main call of compile_smart.
- Fix: on function with parameter, it is impossible to give a list (because parameter is split with `,`)