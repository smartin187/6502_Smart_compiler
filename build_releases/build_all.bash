#!/bin/bash

# This script compile all scripts in executable

cd ..

if [ -d "build_publish" ]; then
    echo "Remove the old build_publish directory"
    rm -r build_publish
fi

mkdir -p build_publish

./build_releases/build_linux/build_all_linux.bash

echo "Compillation finished. Executable files are in the build_publish directory."
