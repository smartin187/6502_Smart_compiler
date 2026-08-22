#!/bin/bash

# This script make a Windows executable from Wine, to make executable for Windows from Linux.

# carful: the compilation can fail

# Need wine, and Pyinstaller on wine.

set -e

mkdir -p build_publish/windows/

# ---- build main.py ----

wine pyinstaller --onefile main.py

cp dist/main.exe build_publish/windows/smart_compiler.exe

# ---- build smart_emulator.py ----

wine pyinstaller --onefile --add-data "img/logo_smart_small.png;." smart_emulator.py

cp dist/smart_emulator.exe build_publish/windows/smart_emulator.exe
