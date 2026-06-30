"""
This programme is for test all functionalities of smart.
"""
import os

import smart_emulator
from smart_compiller import compile_smarty
from compiller_tool.color_tool import Colors
from compiller_tool.smart_exception import SmartError

class TestError(Exception):
    """Mian Exception for test."""
    pass

class StopTest(TestError):
    """This exception is for stop the test."""
    pass

class OutputError(TestError):
    """If the output of programme are not good."""
    pass

class Test:
    """This class is for testing all functionalities of smart."""
    def __init__(self, name:str, code:str, output:str="", compile_output:str="", compile_only:bool=False, sucess:bool=True):
        self.name = name
        self.code = code
        self.compile_only = compile_only
        self.output = output + "\n\nEnd of run"
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

            if self.code_compile != self.compile_output:
                if self.compile_only:
                    raise OutputError(f"The output of compilation is not good:\n{self.code_compile}")
                else:
                    print(f"{Colors.YELLOW}Warning: hex compilation of Smart programme is not normal{Colors.RESET}")

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
                    output = smart_emulator.start_test(self.code_compile)

                    if output != self.output:
                        raise OutputError(f"The output of programme is not good:\n{output}")

                except OutputError as oe:
                    error = True
                    error_output = str(oe)

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

syntaxe_error_test = [  # this test have the same class Test but for test sintaxe error.
    Test(
        "Forget ';'",
        code='print: "TEST"\nprint: "ERROR"',
        compile_only=True,
        sucess=False
    ),
    Test(
        "Unclosed str",
        code="print: \"TEST",
        compile_only=True,
        sucess=False
    ),
    Test(
        "Bad char in str",
        code='print: "a"',
        compile_only=True,
        sucess=False
    ),
    Test(
        "Sintaxe error after str",
        code='print: "HELLO" error',
        compile_only=True,
        sucess=False
    )
]


tests = [

    Test(
        "Test print",
        code='print: "PRINT TEST";',
        compile_output="0400: A9 50 20 EF FF A9 52 20 EF FF A9 49 20 EF FF A9 4E 20 EF FF A9 54 20 EF FF A9 20 20 EF FF A9 54 20 EF FF A9 45 20 EF FF A9 53 20 EF FF A9 54 20 EF FF 00 ",
        output="PRINT TEST"
    ),
    Test(
        "Variable test",
        code="""
.a = 'A';
.b = 'B';
print: .a;
print: .b;

.a = .b;
print: .a;
.b = 64;
print: .b;
""",
        compile_output="0400: A9 41 8D 00 03 A9 42 8D 01 03 AD 00 03 20 EF FF AD 01 03 20 EF FF AD 01 03 8D 00 03 AD 00 03 20 EF FF A9 40 8D 01 03 AD 01 03 20 EF FF 00 ",
        output="ABB@"
    )
]

global_tests = syntaxe_error_test + tests

for test in global_tests:
    test.run()

if all_ok:
    print(f"{Colors.BG_GREEN}All tests without error!{Colors.RESET}")
else:
    print(
        f"{Colors.BG_RED}Some tests failed!{Colors.RESET}",
        f"{Colors.RED}Error: {error_counter}/{len(tests)}{Colors.RESET}",
    )