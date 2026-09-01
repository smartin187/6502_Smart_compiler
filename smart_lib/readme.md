# Smart library

The library for Smart. They are global library and Smart library (system of Smart).

## Path of library

On Linux:

- **Global library**: /usr/lib/Smart-SmartyKit/global_lib/
- **Smart library**: /usr/lib/Smart-SmartyKit/smart_lib/

On Windows:

- **Global library**: C:\Users\you\AppData\Local\Smart-SmartyKit\lib\global_lib\
- **Smart library**: C:\Users\you\AppData\Local\Smart-SmartyKit\lib\smart_lib\

To use the library, copy the folders `global_lib` and `smart_lib` to your library path.

## Add your library to project

If you make a new library, you can do a pull request to GitHub repository.

### Make a library

On the folder `smart_lib` or `global_lib`, please make a directory with the name of library, and set the code of Smart in your directory. If you have a big library, you can split your code into different files for easier use.

When you use your library, the code is:

```smart
import "name_of_library/name_of_file.sma"
```

> Because you need to make a directory for your library, do not forget to set the directory name (`name_of_library` in the example).

### Documentation of library

If you make a library for Smart, you can add a documentation `readme.md` in the folder of your library. (see [make a library](#make-a-library)).

### About licence

The licence of Smart is Apache License, version 2.0.

By default, your library will have this licence. If you want to change the licence, add a `licence.txt` file.

> Your licence muste be open source and compatible with Apache 2.0...
