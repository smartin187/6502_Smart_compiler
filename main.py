# -*- coding: utf-8 -*-

"""
Main module of Smart compiller.
"""

from sys import argv
import sys
import traceback
from smart_compiller import SmartError, CompileError, compile_smarty
import logging

from compiller_tool import smart_info

if "--help" in argv:
    print(smart_info.SMART_HELP["smart_compiller"])
    sys.exit(0)
elif "--version" in argv:
    print(smart_info.SMART_VERSION)
    sys.exit(0)

CODE_ADRESSE = 1024

if "--bin" in argv: # make a binary file
    argv.remove("--bin")

    bin_file = True

else:
    bin_file = False

if len(argv) == 1:
    raise Exception("Error : no source was givent")

try:
    compile_smarty(argv[1], argv, CODE_ADRESSE, bin_outpout_file=bin_file)
except SmartError:
    sys.exit(1)

except KeyboardInterrupt:
    logging.critical("User keyboard interrupt")

except CompileError:
    sys.exit(1)

except:
    logging.critical("Error during build")
    print(traceback.format_exc())
    sys.exit(1)
