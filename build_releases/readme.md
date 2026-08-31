# Build releases

For distributing Smart, this script uses `pyinstaller` to make executable files from Python scripts.

To compile all scripts, use the [`build_all.bash`](./build_all.bash) script.

At the end you get executable files, in the directory `build_publish`.

**If you have a problem with this script**, report an issue on GitHub.

> The script `build_all.bash` needs to be run on Linux, with Debian or Debian-based. If you need only to compile for Windows from Windows, see [build only one Windows from Windows](#build-only-one-windows-from-windows) section.

> **If you have problems with dependencies, see the [dependencies](#dependencies) section.**

The easiest is `build_all.bash`, but you can use another script if you don't want to compile everything:

## Build all

Use the script [`build_all.bash`](./build_all.bash) to compile all scripts, and make a Debian package.

> Warning: if you don't use `build_all.bash`, you need to make the directory `build_publish` before running the scripts (recommended to have a clean directory).

### Build only one Linux

Use the script [`build_linux/build_all_linux.bash`](./build_linux/build_all_linux.bash) to compile all scripts for Linux, and make a Debian package.

#### Build only binary Linux

If you want only the binary files (not the Debian package), use the script [`build_linux/build_linux.bash`](./build_linux/build_linux.bash).

#### Build only Debian package Linux

> Warning: you need to run the script [`build_linux/build_linux.bash`](./build_linux/build_linux.bash) before, to make the binary files.

Run the script [`build_linux/build_deb.bash`](./build_linux/build_deb.bash) to make the Debian package.

#### Build for other architecture Linux

If your computer is `amd64` / `x86_64`, you can compile for `arm64` / `aarch64` architecture, and vice versa.

Use the script [`build_linux/build_other_architecture.bash`](./build_linux/build_other_architecture.bash) to compile all scripts for the other architecture.

> This script is also run with [build_all.bash](./build_all.bash).

> Careful: this script takes a long time to compile.

You need Docker installed.

> It also makes a Debian package for the other architecture.

##### Speed up

You can use the script [`build_docker.sh`](./build_linux/docker_build/build_docker.sh) to build a Docker image (named smart-builder). Then the script `build_other_architecture.bash` uses this image to compile faster (pyinstaller is already installed on this image). This script uses the image `python:3.12-bookworm` to build the image smart-builder, with the [`Dockerfile`](./build_linux/docker_build/Dockerfile)

### Build only one Windows

> This script is run on Linux. If you need to compile for Windows from Windows, see [build only one Windows from Windows](#build-only-one-windows-from-windows) section.

Use the script [`build_wine/build_wine.bash`](./build_wine/build_wine.bash) to compile all scripts for Windows, from Linux, using Wine.

Run this script to make the executable files for Windows, and make a zip archive with the executable file and the Smart library.

You need Wine installed, and Pyinstaller on Wine.

## Build only one Windows from Windows

Other scripts can run only on Linux. But if you need only to compile for Windows from Windows, use the script [`build_on_windows/build_windows.bat`](./build_on_windows/build_windows.bat).

You need to have Python 3 and Pyinstaller installed on Windows.

The `bat` gives the `exe` files in `build_publish\windows` directory.

If you want to compile manually, the command is the same as on Linux:

```bash
pyinstaller --onefile main.py
```

## Dependencies

Run `check_dependencies.bash` to automatically check the dependencies.

The following dependencies are required to build the releases:

- `pyinstaller` (needs Python 3)
- `dpkg-deb`, needs Debian or Debian-based Linux to have `dpkg`.

### Install dependencies

> If a dependency is missing, the script `check_dependencies.bash` can install it. `dpkg` can't be installed automatically...

#### Pyinstaller

You need Python 3 first, and make sure you have `pip` or `pip3` installed.

To install `pyinstaller`, run the command:

```bash
pip install pyinstaller
```

> If the command fails, replace `pip` by `pip3` in the command.

Verify with:

```bash
pyinstaller --version
```

#### Dpkg

You need a Debian or Debian-based Linux to have `dpkg` installed.

If you don't have a Debian or Debian-based system, you can try a virtual machine or Docker.

#### Wine

To compile for Windows from Linux, you can use Wine.

You need Wine installed.

Moreover, you need to install Pyinstaller on Wine (and Python 3).

##### Install Pyinstaller

Install Python 3 on Wine, and make sure you have `pip` installed.

Next, install Pyinstaller on Wine:

```bash
wine pip install pyinstaller
```

Verify with:

```bash
wine pyinstaller --version
```

#### Docker

To compile for other architectures, you need Docker installed.

Install with:


```bash
sudo apt install docker.io
```

Verify with:

```bash
docker --version
```

#### zip

For Windows, you need `zip` to make a zip archive with the executable file and the Smart library.

Install with:

```bash
sudo apt install zip
```

Verify with:

```bash
zip --version
```
