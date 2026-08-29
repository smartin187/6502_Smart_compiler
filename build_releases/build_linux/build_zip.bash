#!/bin/bash

# this script make a archive zip for the Linux executable

# set on argument: tag (Linux-amd64 or Linux-arm64) then the directory name of architecture

echo -e "\033[1m---- Building zip archive for Linux... ----\033[0m"

TAG=$1
ARCH_DIR_DIST=$2

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
