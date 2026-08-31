# -*- coding: utf-8 -*-

"""
Has the version of Smart and the help.
"""
import sys
from compiller_tool.color_tool import Colors

FROZEN = getattr(sys, 'frozen', False)  # if the programme is compiled by PyInstaller

SMART_VERSION = "v0.0.7"

ONE_LINUX = sys.platform == "linux"

EXECUTABLE = {
    "compiller":"smart_compiler" if ONE_LINUX else "smart_compiler.exe",
    "emulator":"smart_emulator" if ONE_LINUX else "smart_emulator.exe"
}

LICENCE = {
    "licence":"Apache License 2.0",
    "text":"""Copyright (c) 2026 smartin178

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""
}

GIT_HUB_LINK = "https://github.com/smartin187/smartykit_compiler"

COMPILE_EXE = EXECUTABLE["compiller"] if FROZEN else "python3 main.py"
EMULATOR_EXE = EXECUTABLE["emulator"] if FROZEN else "python3 smart_emulator.py"

SMART_HELP = {
    "smart_compiller":f"""\t\t{Colors.BG_BLUE}Welcome to Smart {SMART_VERSION}{Colors.RESET}

{Colors.BG_CYAN}Help:{Colors.RESET}
\tCompile your programme: {Colors.MAGENTA}{COMPILE_EXE} your_programme.sma{Colors.RESET}

{Colors.BG_CYAN}FLAGS:{Colors.RESET}
\tGet a binary file (default is hex file): {Colors.MAGENTA}{COMPILE_EXE} your_programme.sma --bin{Colors.RESET}
\tRegroup bytes in the output file (for hex file): {Colors.MAGENTA}{COMPILE_EXE} your_programme.sma --regroup=number{Colors.RESET}\t\t{Colors.YELLOW}Set -1 (by default) for no regroup.{Colors.RESET}
\tShow the library path: {Colors.MAGENTA}{COMPILE_EXE} --show-lib-path{Colors.RESET}
\tGet version of Smart: {Colors.MAGENTA}{COMPILE_EXE} --version{Colors.RESET}
\tGet help of Smart Compiller: {Colors.MAGENTA}{COMPILE_EXE} --help{Colors.RESET}
\tGet the licence of Smart: {Colors.MAGENTA}{COMPILE_EXE} --show-licence{Colors.RESET}

{Colors.BG_CYAN}GitHub:{Colors.RESET} {GIT_HUB_LINK}

See also the Smart Emulator: {Colors.MAGENTA}{EMULATOR_EXE} --help{Colors.RESET}

""",
    "smart_emulator":f"""\t\t{Colors.BG_BLUE}Welcome to Smart Emulator {SMART_VERSION}{Colors.RESET}
You can run and debug your programme with emulator.

{Colors.BG_CYAN}Help:{Colors.RESET}
\tOpen emulator (with a graphical interface): {Colors.MAGENTA}{EMULATOR_EXE}{Colors.RESET}\t\t{Colors.YELLOW}With GUI, you can open a hex file ({Colors.BOLD}compilled Smart recommended{Colors.RESET}{Colors.YELLOW}).{Colors.RESET}
\tRun your programme: {Colors.MAGENTA}{EMULATOR_EXE} your_programme.sma{Colors.RESET}

{Colors.BG_CYAN}FLAGS:{Colors.RESET}
\tRun hex programme, you will write your hex on the entry: {Colors.MAGENTA}{EMULATOR_EXE} --hex-entry{Colors.RESET}
\tRun programme on debug mode: {Colors.MAGENTA}{EMULATOR_EXE} your_programme.sma --debug{Colors.RESET}
\tRun the emulator on console (no GUI): {Colors.MAGENTA}{EMULATOR_EXE} your_programme.sma --console{Colors.RESET}
\tGet version of Smart: {Colors.MAGENTA}{EMULATOR_EXE} --version{Colors.RESET}
\tGet help of Smart Emulator: {Colors.MAGENTA}{EMULATOR_EXE} --help{Colors.RESET}
\tGet the licence of Smart: {Colors.MAGENTA}{EMULATOR_EXE} --show-licence{Colors.RESET}

{Colors.BG_CYAN}GitHub:{Colors.RESET} {GIT_HUB_LINK}

See also the Smart Compiller: {Colors.MAGENTA}{COMPILE_EXE} --help{Colors.RESET}

    """
}


