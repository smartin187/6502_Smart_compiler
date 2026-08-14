# Build releases

For distributing Smart, this script use `pyinstaller` for make executable files from Python scripts.

For compile all scripts, use the [`build_all.bash`](./build_all.bash) script.

At the end you get executable files, on the directory `build_publish`.

> **If you have probleme with dependencies, see [dependencies](#dependencies) section.**

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

## Dependencies

Run `check_dependencies.bash` for auto check the dependencies.

The following dependencies are required for build the releases:

- `pyinstaller` (need Python 3)
- `dpkg-deb`, need Debian or Debian-based Linux for have `dpkg`.

### Install dependencies

> If a missing dependency, the script `check_dependencies.bash` can install it. `dpkg` and `wine` can't be installed automatically...

#### Pyinstaller

You need before Python 3, and make sure have `pip` or `pip3` installed.

For install `pyinstaller`, run the command:

```bash
pip install pyinstaller
```

> If command fail, replace `pip` by `pip3` in the command.

Verify with:

```bash
pyinstaller --version
```

#### Dpkg

You need a Debian or Debian-based Linux for have `dpkg` installed.

If you don't have a Debian orDebian-based, you can try a virtual machine or Docker.

#### Wine

For compile for Windows from Linux, you can use Wine.

You need Wine installed.

Moreover, you need to install Pyinstaller on Wine (and Python 3).

##### Install Pyinstaller

Install Python 3 on Wine, and make sure have `pip` installed.

Next install Pyinstaller on Wine:

```bash
wine pip install pyinstaller
```

Verify with:

```bash
wine pyinstaller --version
```
