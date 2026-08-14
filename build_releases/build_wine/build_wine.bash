#!/bin/bash

# This script make a Windows executable from Wine, to make executable for Windows from Linux.

# carful: the compilation can fail

# Need wine, and Pyinstaller on wine.

mkdir -p build_publish/windows/

# ---- build main.py ----

wine pyinstaller --onefile main.py

cp dist/main build_publish/linux/smart_compiler

# ---- build smart_emulator.py ----

wine pyinstaller --onefile smart_emulator.py

cp dist/smart_emulator build_publish/linux/smart_emulator
