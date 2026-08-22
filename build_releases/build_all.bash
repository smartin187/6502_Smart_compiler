#!/bin/bash

# This script compile all scripts in executable

set -e

cd ..

if [ -d "build_publish" ]; then
    echo "Remove the old build_publish directory"
    sudo rm -r build_publish
fi

mkdir -p build_publish

./build_releases/build_linux/build_all_linux.bash

./build_releases/build_wine/build_wine.bash

echo "Cleaning up"
rm -r dist

echo "Compilation finished. Executable files are in the build_publish directory."
