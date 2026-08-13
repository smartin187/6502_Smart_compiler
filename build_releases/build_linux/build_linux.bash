#!/bin/bash

# For make executable binary for Linux.
# It compile `main.py` and `smart_emulator.py`

mkdir -p build_publish/linux/

# ---- build main.py ----

pyinstaller --onefile main.py

cp dist/main build_publish/linux/smart_compiler

# ---- build smart_emulator.py ----

pyinstaller --onefile smart_emulator.py

cp dist/smart_emulator build_publish/linux/smart_emulator