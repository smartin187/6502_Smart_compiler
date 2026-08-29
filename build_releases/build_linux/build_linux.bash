#!/bin/bash

# For make executable binary for Linux.
# It compile `main.py` and `smart_emulator.py`

set -e

ARCH_DIR_DIST=$(dpkg --print-architecture)
TAG="Linux-${ARCH_DIR_DIST}"

echo -e "\033[1m---- Build for Linux $ARCH_DIR_DIST... ----\033[0m"

mkdir -p build_publish/linux/$ARCH_DIR_DIST/

# ---- build main.py ----

pyinstaller --onefile main.py

cp dist/main build_publish/linux/$ARCH_DIR_DIST/smart_compiler_$TAG

# ---- build smart_emulator.py ----

pyinstaller --onefile --add-data "img/logo_smart_small.png:." smart_emulator.py

cp dist/smart_emulator build_publish/linux/$ARCH_DIR_DIST/smart_emulator_$TAG

# ---- build a zip file ----

mkdir -p build_publish/linux/$ARCH_DIR_DIST/archive_zip/

# copy the executable
cp build_publish/linux/$ARCH_DIR_DIST/smart_compiler_$TAG build_publish/linux/$ARCH_DIR_DIST/archive_zip/
cp build_publish/linux/$ARCH_DIR_DIST/smart_emulator_$TAG build_publish/linux/$ARCH_DIR_DIST/archive_zip/

# copy library

cp -r smart_lib/ build_publish/linux/$ARCH_DIR_DIST/archive_zip/

# set a readme:
echo "Smart Compiler and Emulator for Windows
You get smart_compiler and smart_emulator for Linux.
You have also the Smart library. Please copy the directory to /usr/lib/Smart-SmartyKit/

Apache License 2.0
See https://github.com/smartin187/smartykit_compiler for more information.
" > build_publish/linux/$ARCH_DIR_DIST/archive_zip/readme.txt

# build zip
cd build_publish/linux/$ARCH_DIR_DIST/
zip -r Smart_$TAG.zip archive_zip/

cd ../../..

rm -r build_publish/linux/$ARCH_DIR_DIST/archive_zip/
