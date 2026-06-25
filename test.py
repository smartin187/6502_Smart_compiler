"""
This programme is for test all functionalities of smart.
"""
import os

import smart_emulator
from smart_compiller import compile_smarty

class Test:
    """This class is for testing all functionalities of smart."""
    def __init__(self, name:str, code:str, output:str, compile_output:str, compile_only:bool=False):
        self.name = name
        self.code = code
        self.compile_only = compile_only
        self.output = output
        self.compile_output = compile_output

    def run(self):
        """This function is for running the test."""
        with open("test/test.sma", "w") as f:
            f.write(self.code)

        self.code_compile = compile_smarty("test/test.sma", make_file=False)

        smart_emulator.start_test(self.code_compile)

smart_emulator.GUI_MODE = False
smart_emulator.on_test = True

os.makedirs("test", exist_ok=True)

all_ok = True


tests = [
    Test(
        "Test print",
        code="""
        print: "HELLO";
        """,
        compile_output="0400: A9 48 20 EF FF A9 45 20 EF FF A9 4C 20 EF FF A9 4C 20 EF FF A9 4F 20 EF FF 00",
        output="HELLO"
    )
]

for test in tests:
    test.run()
