#!/bin/bash

# This script compile and package all for Linux.

./build_releases/build_linux/build_linux.bash   # make the executable binary
./build_releases/build_linux/build_deb.bash     # make the deb package

./build_releases/build_linux/build_other_architecture.bash   # make the executable binary for the other architecture
