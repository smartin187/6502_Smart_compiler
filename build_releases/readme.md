# Build releases

For distributing Smart, this script use `pyinstaller` for make executable files from Python scripts.

For compile all scripts, use the [`build_all.bash`](./build_all.bash) script.

At the end you get executable files, on the directory `build_publish`.

**If you have probleme with this script**, report a issue on GitHub.

> The script `build_all.bash` need to be run on Linux, with Debian or Debian-based. If you need only to compile for Windows from Windows, see [build only one Windows from Windows](#build-only-one-windows-from-windows) section.

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

#### Build for other architecture Linux

If your computer is `amd64` / `x86_64`, you can compile for `arm64` / `aarch64` architecture, and vice versa.

Use the script [`build_linux/build_other_architecture.bash`](./build_linux/build_other_architecture.bash) for compile all scripts for other architecture.

> This script is also run with [build_all.bash](./build_all.bash).

> Carful: this script take a long time for compile.

You need Docker installer.

> Make also a Debian package for the other architecture.

##### Speed up

You can use the script [`build_docker.sh`](./build_linux/docker_build/build_docker.sh) for build an image Docker (named smart-builder). Next the script `build_other_architecture.bash` use this image for compile faster (pyinstaller is already installed on this image). This script use the image `python:3.12-bookworm` for build the image smart-builder, with the [`Dockerfile`](./build_linux/docker_build/Dockerfile) 

### Build only one Windows

> This script is run on Linux. If you need to compile for Windows from Windows, see [build only one Windows from Windows](#build-only-one-windows-from-windows) section.

Use the script [`build_wine/build_wine.bash`](./build_wine/build_wine.bash) for compile all scripts for Windows, from Linux, using Wine.

Run this script for make the executable files for Windows.

You need Wine installed, and Pyinstaller on Wine.

## Build only one Windows from Windows

Other script can run only on Linux. But if you need only to compile for Windows from Windows, use the script [`build_on_windows/build_windows.bat`](./build_on_windows/build_windows.bat).

You need to have Python 3 and Pyinstaller installed on Windows.

The `bat` give the `exe` files in `build_publish\windows` directory.

If you want to compile manually, the command is the same to Linux:

```bash
pyinstaller --onefile main.py
```

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
