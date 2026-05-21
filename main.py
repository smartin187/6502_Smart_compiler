# -*- coding: utf-8 -*-

"""
Main module of Smart compiller.
"""

from sys import argv
import traceback
from smart_compiller import SmartError, compile_smarty

CODE_ADRESSE = 1024



if len(argv) == 1:
    raise Exception("Error : no source was givent")

try:
    compile_smarty(argv[1], argv, CODE_ADRESSE)
except SmartError:
    quit()

except:
    print("Error during build")
    print(traceback.format_exc())