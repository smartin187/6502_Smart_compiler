# Smart library

The library for Smart. They are global library and Smart library (system of Smart).

## Path of library

On Linux:

- **Global library**: /usr/lib/Smart-SmartyKit/global_lib/
- **Smart library**: /usr/lib/Smart-SmartyKit/smart_lib/

On Windows:

- **Global library**: C:\Users\you\AppData\Local\Smart-SmartyKit\lib\global_lib\
- **Smart library**: C:\Users\you\AppData\Local\Smart-SmartyKit\lib\smart_lib\

For use the library, copy the folder `global_lib` and `smart_lib` to you path for library.

## Make a library

On the folder `smart_lib` or `global_lib`, please make a directory with the name of library, and set the code of Smart in your directory. If you have bit library, if you can split your code in different files for moste easy use.

When you use you library, the code is:

```smart
import "name_of_library/name_of_file.sma"
```

> Because you need to make a directory for your library, do not forget to set the directory name (`name_of_library` on the exemple).

## Documentation of library

If you make a library for Smart, you can add a documentation `readme.md` in the folder of you library. (see [make a library](#make-a-library)).
