#!/bin/bash

# This script make the deb package for Linux, of smart compiler and smart emulator.

# for the architecture, you can specify it as the first argument, or it will be detected automatically.

set -e

VERSION="1.0"
ARCH="${1:-$(dpkg --print-architecture)}"

# Make the structure

mkdir -p build_publish/tmp_deb/DEBIAN/
mkdir -p build_publish/tmp_deb/usr/bin/

echo -e "Package: smart-compiler-emulator\nVersion: ${VERSION}\nSection: development\nPriority: optional\nArchitecture: ${ARCH}\nDepends:\nMaintainer: smartin187 <smartin187>\nDescription: The Smart Compiler and Smart Emulator\n" > build_publish/tmp_deb/DEBIAN/control

# copy the compiller and emulator

cp build_publish/linux/${ARCH}/smart_compiler build_publish/tmp_deb/usr/bin/smart_compiler
cp build_publish/linux/${ARCH}/smart_emulator build_publish/tmp_deb/usr/bin/smart_emulator

# copy the libraries

mkdir -p build_publish/tmp_deb/usr/lib/Smart-SmartyKit/global_lib
mkdir -p build_publish/tmp_deb/usr/lib/Smart-SmartyKit/smart_lib

cp -a smart_lib/global_lib/. build_publish/tmp_deb/usr/lib/Smart-SmartyKit/global_lib/
cp -a smart_lib/smart_lib/. build_publish/tmp_deb/usr/lib/Smart-SmartyKit/smart_lib/

# build package

dpkg-deb --build --root-owner-group build_publish/tmp_deb build_publish/linux/${ARCH}/smart-compiler-emulator_${VERSION}_${ARCH}.deb

rm -r build_publish/tmp_deb
