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
            echo "pyinstaller installed successfully.
Restart the script for check other dependencies."
            exit 0
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

# Wine

if wine --version > /dev/null 2>&1; then
    echo "wine    OK"
else
    echo "wine is not installed. You need to install wine to build Windows executable from Linux."
    # auto install
    read -p "Do you want to install wine? (y/n) " answer

    if [[ "$answer" == "y" ]]; then
        if sudo apt update && sudo apt install wine; then
            echo "wine installed successfully.
Restart the script for check other dependencies."
            exit 0
        else
            echo "Failed to install wine (command 'sudo apt update && sudo apt install wine'). Please install it manually."
            exit 1
        fi
    else
        exit 1
    fi
    exit 1
fi

# pyinstaller on wine

if wine pyinstaller --version > /dev/null 2>&1; then
    echo "pyinstaller on wine    OK"
else
    echo "pyinstaller on wine is not installed. You need to install pyinstaller on wine to build Windows executable from Linux."
    # auto install
    read -p "Do you want to install pyinstaller on wine? (y/n) " answer

    if [[ "$answer" == "y" ]]; then
        if wine pip install pyinstaller; then
            echo "pyinstaller on wine installed successfully.
Restart the script for check other dependencies."
            exit 0
        else
            echo "Failed to install pyinstaller on wine (command 'wine pip install pyinstaller'). Please install it manually."
            exit 1
        fi
    else
        exit 1
    fi

    exit 1
fi

# zip

if zip --version > /dev/null 2>&1; then
    echo "zip    OK"
else
    echo "zip is not installed. You need to install zip for make archive for Windows."
    # auto install
    read -p "Do you want to install zip? (y/n) " answer

    if [[ "$answer" == "y" ]]; then
        if sudo apt update && sudo apt install zip; then
            echo "zip installed successfully.
Restart the script for check other dependencies."
            exit 0
        else
            echo "Failed to install zip (command 'sudo apt update && sudo apt install zip'). Please install it manually."
            exit 1
        fi
    else
        exit 1
    fi

    exit 1
fi

# docker

if docker --version > /dev/null 2>&1; then
    echo "Docker    OK"
else
    echo "Docker is not installed. You need to install Docker to build for other architectures for Linux."
    # auto install
    read -p "Do you want to install Docker? (y/n) " answer

    if [[ "$answer" == "y" ]]; then
        if sudo apt update && sudo apt install docker.io; then
            echo "Docker installed successfully.
Restart the script for check other dependencies."
            exit 0
        else
            echo "Failed to install Docker (command 'sudo apt update && sudo apt install docker.io'). Please install it manually."
            exit 1
        fi
    else
        exit 1
    fi

    exit 1
fi






echo "All dependencies are satisfied."