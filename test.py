"""
This programme is for test all functionalities of smart.
"""
import os

import smart_emulator
from smart_compiller import compile_smarty
from compiller_tool.color_tool import Colors
from compiller_tool.smart_exception import SmartError

class StopTest(Exception):
    """This exception is for stop the test."""
    pass

class Test:
    """This class is for testing all functionalities of smart."""
    def __init__(self, name:str, code:str, output:str, compile_output:str, compile_only:bool=False, sucess:bool=True):
        self.name = name
        self.code = code
        self.compile_only = compile_only
        self.output = output
        self.compile_output = compile_output
        self.sucess = sucess
    
    def show_test(self, start_compilation:bool=True) -> None:
        """Print the detail of test"""
        print(
            f"{Colors.BG_BLUE}\t\tTest: {self.name}{Colors.RESET}",
            f"{Colors.GREEN}INFO:{Colors.RESET}",
            f"Compile only: {self.compile_only}",
            f"Normal sucess: {self.sucess}",
            f"{Colors.YELLOW}Starting compilation...{Colors.RESET}" if start_compilation else "",

            sep="\n"
        )


    def run(self) -> None:
        """This function is for running the test."""
        global all_ok, error_counter

        with open("test/test.sma", "w") as f:
            f.write(self.code)

        self.show_test()

        error = False
        error_output = ""
        compilation_error = False

        try:
            self.code_compile = compile_smarty("test/test.sma", make_file=False)
        except SmartError as se:
            error = True
            compilation_error = True
            error_output = str(se)
        
        except Exception as e:
            error = True
            error_output = "Smart Emulator error: " + str(e)
        
        else:
            if not self.compile_only:
                try:
                    smart_emulator.start_test(self.code_compile)
                except Exception as e:
                    error = True
                    error_output = str(e)
        
        if error and self.sucess:
            all_ok = False
            error_counter += 1

            print(
                f"{Colors.BG_RED}ERROR: Test failed{Colors.RESET}",
                f"{Colors.RED}{'Compilation error' if compilation_error else 'Runtime error'}",
                f"Error output: {error_output}{Colors.RESET}",

                sep="\n"
            )

            reply = input("Continue test ? (y/n): ")

            if reply.lower() == "n":
                raise StopTest("Test stopped by user")
        
            print(end="\n"*10)
        
        else:
            print(f"{Colors.BG_GREEN}Test OK{Colors.RESET}", end="\n"*10)

        

smart_emulator.GUI_MODE = False
smart_emulator.on_test = True

os.makedirs("test", exist_ok=True)

all_ok = True
error_counter = 0


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

if all_ok:
    print(f"{Colors.BG_GREEN}All tests without error!{Colors.RESET}")
else:
    print(
        f"{Colors.BG_RED}Some tests failed!{Colors.RESET}",
        f"{Colors.RED}Error: {error_counter}/{len(tests)}{Colors.RESET}",
    )