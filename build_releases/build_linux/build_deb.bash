#!/bin/bash

# This script make the deb package for Linux, of smart compiler and smart emulator.

set -e

VERSION="1.0"
ARCH=$(dpkg --print-architecture)

# Make the structure

mkdir -p build_publish/tmp_deb/DEBIAN/
mkdir -p build_publish/tmp_deb/usr/bin/

echo -e "Package: smart-compiler-emulator\nVersion: ${VERSION}\nSection: development\nPriority: optional\nArchitecture: ${ARCH}\nDepends:\nMaintainer: smartin187 <smartin187>\nDescription: The Smart Compiler and Smart Emulator\n" > build_publish/tmp_deb/DEBIAN/control

# copy the compiller and emulator

cp build_publish/linux/smart_compiler build_publish/tmp_deb/usr/bin/smart_compiler
cp build_publish/linux/smart_emulator build_publish/tmp_deb/usr/bin/smart_emulator

# copy the libraries

mkdir -p build_publish/tmp_deb/usr/lib/Smart-SmartyKit/global_lib
mkdir -p build_publish/tmp_deb/usr/lib/Smart-SmartyKit/smart_lib

cp -a smart_lib/global_lib/. build_publish/tmp_deb/usr/lib/Smart-SmartyKit/global_lib/
cp -a smart_lib/smart_lib/. build_publish/tmp_deb/usr/lib/Smart-SmartyKit/smart_lib/

# build package

dpkg-deb --build build_publish/tmp_deb build_publish/linux/smart-compiler-emulator_${VERSION}_${ARCH}.deb

rm -r build_publish/tmp_deb
