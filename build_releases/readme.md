# Build releases

For distributing Smart, this script use `pyinstaller` for make executable files from Python scripts.

For compile all scripts, use the [`build_all.bash`](./build_all.bash) script.

At the end you get executable files, on the directory `build_publish`.

The most easy is `build_all.bash`, but you can use other script if you don't like to compile for all:

## Build all

Use the script [`build_all.bash`](./build_all.bash) for compile all scripts, and make Debian package.

> Warning: if you don't use `build_all.bash`, you need to make the directory `build_publish` before run the scripts (recommended to have a clean directory).

### Build only one Linux

Use the script [`build_linux/build_all_linux.bash`](./build_linux/build_all_linux.bash) for compile all scripts for Linux, and make Debian package.

#### Build only binary Linux

If you want only the binary files (not Debian package), use the script [`build_linux/build_linux.bash`](./build_linux/build_linux.bash).

#### Build only Debian package Linux

> Warning: you need to run before the script [`build_linux/build_linux.bash`](./build_linux/build_linux.bash) for make the binary files.

Run the script [`build_linux/build_deb.bash`](./build_linux/build_deb.bash) for make the Debian package.

