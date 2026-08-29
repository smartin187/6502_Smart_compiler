#!/bin/bash

# This script make a Windows executable from Wine, to make executable for Windows from Linux.

# carful: the compilation can fail

# Need wine, and Pyinstaller on wine.

echo -e "\033[1m---- Build with Wine (build for Windows)... ----\033[0m"

set -e

mkdir -p build_publish/windows/

# ---- build main.py ----

wine pyinstaller --onefile main.py

cp dist/main.exe build_publish/windows/smart_compiler.exe

# ---- build smart_emulator.py ----

wine pyinstaller --onefile --add-data "img/logo_smart_small.png;." smart_emulator.py

cp dist/smart_emulator.exe build_publish/windows/smart_emulator.exe

# ---- build a zip file ----

mkdir -p build_publish/windows/archive_zip/

# copy the executable
cp build_publish/windows/smart_compiler.exe build_publish/windows/archive_zip/
cp build_publish/windows/smart_emulator.exe build_publish/windows/archive_zip/

# copy library

cp -r smart_lib/ build_publish/windows/smart_emulator.exe build_publish/windows/archive_zip/

# set a readme:
echo "Smart Compiler and Emulator for Windows
You get smart_compiler.exe and smart_emulator.exe.
You have also the Smart library. Please copy the directory to C:\\users\\you\\AppData\\Local\\Smart-SmartyKit\\lib\\

Apache License 2.0
See https://github.com/smartin187/smartykit_compiler for more information.
" > build_publish/windows/archive_zip/readme.txt

# build zip
cd build_publish/windows/
zip -r Smart-Windows.zip archive_zip/

cd ../..

rm -r build_publish/windows/archive_zip/


