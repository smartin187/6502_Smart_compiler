#!/bin/bash

# This script compile and package for the architecture arm64 or amd64.
# If your computer is amd64, this script build for arm64, if you computer is arm64, this script build for amd64.

# RUN THIS COMMAND BEFORE : sudo docker run --privileged --rm tonistiigi/binfmt --install amd64,arm64

ARCH=$(dpkg --print-architecture)

echo "--- Building for architecture: $ARCH ---"

if [ "$ARCH" = "arm64" ]; then   # make the executable binary for amd64
    sudo docker run --rm \
        --platform linux/amd64 \
        -v "$PWD":/src \
        -w /src \
        python:3.12-bookworm \
        /bin/bash -lc '
            set -eux
            python -m pip install pyinstaller
            bash ./build_releases/build_linux/build_linux.bash
        '

elif [ "$ARCH" = "amd64" ]; then   # make the executable binary for arm64
    sudo docker run --rm \
        --platform linux/arm64 \
        -v "$PWD":/src \
        -w /src \
        python:3.12-bookworm \
        /bin/bash -lc '
            set -eux
            python -m pip install pyinstaller
            bash ./build_releases/build_linux/build_linux.bash
        '
else
    echo "Unsupported architecture: $ARCH, skipping build for other architecture..."
fi

