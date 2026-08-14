#!/bin/bash

# This script test the dependencies needed.

# pyinstaller

if pyinstaller --version > /dev/null 2>&1; then
    echo "pyinstaller    OK"
else
    echo "pyinstaller is not installed. Run 'pip install pyinstaller' to install it."

    # auto install
    read -p "Do you want to install pyinstaller? (y/n) " answer
    if [[ "$answer" == "y" ]]; then
        if pip3 install pyinstaller; then
            echo "pyinstaller installed successfully."
        else
            echo "Failed to install pyinstaller (command 'pip3 install pyinstaller'). Please install it manually."
            exit 1
        fi
    else
        exit 1
    fi
fi

# dpkg

if dpkg-deb --version > /dev/null 2>&1; then
    echo "dpkg-deb (Debian or Debian-based)    OK"
else
    echo "dpkg-deb is not installed. You need a Debian or Debian-based system. Use virtual machine or Docker."
    exit 1
fi

echo "All dependencies are satisfied."
