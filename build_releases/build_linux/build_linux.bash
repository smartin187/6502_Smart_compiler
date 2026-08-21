#!/bin/bash

# For make executable binary for Linux.
# It compile `main.py` and `smart_emulator.py`

set -e

ARCH_DIR_DIST=$(dpkg --print-architecture)

mkdir -p build_publish/linux/$ARCH_DIR_DIST/

# ---- build main.py ----

pyinstaller --onefile main.py

cp dist/main build_publish/linux/$ARCH_DIR_DIST/smart_compiler

# ---- build smart_emulator.py ----

pyinstaller --onefile --add-data "img/logo_smart_small.png:." smart_emulator.py

cp dist/smart_emulator build_publish/linux/$ARCH_DIR_DIST/smart_emulator

