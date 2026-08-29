#!/bin/bash

# This script compile and package for the architecture arm64 or amd64.
# If your computer is amd64, this script build for arm64, if you computer is arm64, this script build for amd64.

echo -e "\033[1m---- Build for Linux for other architecture... ----\033[0m"

sudo docker run --privileged --rm tonistiigi/binfmt --install amd64,arm64

ARCH=$(dpkg --print-architecture)

echo "--- Building for architecture: $ARCH ---"

if [ -d "build/main_cross" ]; then
    echo "Use the cache (main_cross) for cross compilation. In case of error, dellet the cache in build/"
    mv build/main_cross build/main
fi
if [ -d "build/smart_emulator_cross" ]; then
    echo "Use the cache (smart_emulator_cross) for cross compilation. In case of error, dellet the cache in build/"
    mv build/smart_emulator_cross build/smart_emulator
fi

IMAGE_NAME=""
COMMAND_INSTALL=""  # the command for install pyinstaller. Empty if the image smart-builder exist.

if sudo docker image inspect smart-builder:latest >/dev/null 2>&1; then
    echo "Docker image smart-builder:latest already existe, use this image..."
    IMAGE_NAME="smart-builder:latest"
else
    echo -e "warning: Docker image smart-builder:latest does not exist.\nThe build will be longer... Make the Docker image for best performance, see readme.md."
    IMAGE_NAME="python:3.12-bookworm"
    COMMAND_INSTALL="python -m pip install pyinstaller"
fi

if [ "$ARCH" = "arm64" ]; then   # make the executable binary for amd64
    sudo docker run --rm \
        --platform linux/amd64 \
        -v "$PWD":/src \
        -w /src \
        $IMAGE_NAME \
        /bin/sh -c "
            set -eux
            $COMMAND_INSTALL
            sh ./build_releases/build_linux/build_linux.bash
        "
    
    # set on sudo
    sudo ./build_releases/build_linux/build_deb.bash amd64

elif [ "$ARCH" = "amd64" ]; then   # make the executable binary for arm64
    sudo docker run --rm \
        --platform linux/arm64 \
        -v "$PWD":/src \
        -w /src \
        $IMAGE_NAME \
        /bin/sh -c "
            set -eux
            $COMMAND_INSTALL
            sh ./build_releases/build_linux/build_linux.bash
        "
    
    # set on sudo
    sudo ./build_releases/build_linux/build_deb.bash arm64

else
    echo "Unsupported architecture: $ARCH, skipping build for other architecture..."
fi

# save cache for next build

mv build/main build/main_cross
mv build/smart_emulator build/smart_emulator_cross
