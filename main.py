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
elif "--show-lib-path" in sys.argv:
    from compiller_tool.import_tool import show_path_lib
    show_path_lib()
    sys.exit(0)

if "--show-licence" in sys.argv:
    print(smart_info.LICENCE["licence"], smart_info.LICENCE["text"], sep="\n")
    sys.exit(0)

regroup_number = -1

for arg in sys.argv:
    if arg.startswith("--regroup="):
        try:
            regroup_number = int(arg.split("=")[1])
        except:
            logging.critical("Error: regroup number must be an integer")
            sys.exit(1)

        if regroup_number < 1:
            logging.critical("Error: regroup number must be greater than 0, or -1 for no regroup.")
            sys.exit(1)

        sys.argv.remove(arg)
        break
        

CODE_ADRESSE = 1024

if "--bin" in sys.argv: # make a binary file
    sys.argv.remove("--bin")

    bin_file = True

else:
    bin_file = False

if len(sys.argv) == 1:
    logging.critical("Error: no source was givent")
    sys.exit(1)

try:
    compile_smarty(sys.argv[1], sys.argv, CODE_ADRESSE, bin_outpout_file=bin_file, regroup_bytes=regroup_number)
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
