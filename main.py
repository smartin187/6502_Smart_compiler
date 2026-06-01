# -*- coding: utf-8 -*-

"""
Main module of Smart compiller.
"""

import sys
import traceback
from smart_compiller import SmartError, CompileError, compile_smarty
import logging

from compiller_tool import smart_info

if "--help" in sys.argv:
    print(smart_info.SMART_HELP["smart_compiller"])
    sys.exit(0)
elif "--version" in sys.argv:
    print(smart_info.SMART_VERSION)
    sys.exit(0)

CODE_ADRESSE = 1024

if "--bin" in sys.argv: # make a binary file
    sys.argv.remove("--bin")

    bin_file = True

else:
    bin_file = False

if len(sys.argv) == 1:
    raise Exception("Error : no source was givent")

try:
    compile_smarty(sys.argv[1], sys.argv, CODE_ADRESSE, bin_outpout_file=bin_file)
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
