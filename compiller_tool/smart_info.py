# -*- coding: utf-8 -*-

"""
Have the verion of Smart and the help.
"""
import sys

FROZEN = getattr(sys, 'frozen', False)  # if the programme is compiled by Pyinstaller

SMART_VERSION = "v0.0.5"

ONE_LINUX = sys.platform == "linux"

EXECUTABLE = {
    "compiller":"smart_build" if ONE_LINUX else "smart_build.exe",
    "emulator":"smart_emulator" if ONE_LINUX else "smart_emulator.exe"
}

COMPILE_EXE = EXECUTABLE["compiller"] if FROZEN else "python3 main.py"

SMART_HELP = {
    "smart_compiller":f"""Welcome to Smart {SMART_VERSION}.

Help:
\tCompile your programme: {COMPILE_EXE} your_programme.sma
FLAGS:
\tGet a binary file (default is hex file): {COMPILE_EXE} your_programme.sma --bin
\tGet version of Smart: {COMPILE_EXE} --version
\tGet help of Smart Compiller: {COMPILE_EXE} --help

""",
    "smart_emulator":f"""Welcome to Smart Emulator {SMART_VERSION}.
You can run your programme with emulator.

Help:
\tOpen emulator (with a graphical interface): {EXECUTABLE["emulator"]}\t\tWith GUI, you can open a hex file (compilled Smart recommended).
\tRun your programme: {EXECUTABLE["emulator"]} your_programme.sma
\tRun hex programme with entry point: {EXECUTABLE["emulator"]} --hex-entry
\tRun programme on debug mode: {EXECUTABLE["emulator"]} --debug
\tGet version of Smart: {EXECUTABLE["emulator"]} --version
\tGet help of Smart Emulator: {EXECUTABLE["emulator"]} --help
    """
}
