#!/bin/bash

# This script compile and package all for Linux.

MAIN_ARCH_DIR_DIST=$(dpkg --print-architecture)
MAIN_TAG="Linux-${ARCH_DIR_DIST}"

./build_releases/build_linux/build_linux.bash   # make the executable binary
./build_releases/build_linux/build_deb.bash     # make the deb package
./build_releases/build_linux/build_zip.bash ${MAIN_TAG} ${MAIN_ARCH_DIR_DIST}     # make the zip file

./build_releases/build_linux/build_other_architecture.bash   # make the executable binary for the other architecture
