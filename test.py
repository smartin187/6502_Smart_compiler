"""
This programme is for test all functionalities of smart.
"""
import os

import smart_emulator
from smart_compiller import compile_smarty
from compiller_tool.color_tool import Colors
from compiller_tool.smart_exception import SmartError

class TestError(Exception):
    """Main Exception for test."""
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

            if "  " in self.code_compile:
                raise OutputError(f"{Colors.RED}Double space on output. Risk of erorr with adress counting...{Colors.RESET}")

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

        
try:

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
            "Bad char in char",
            code="print: 'a'",
            compile_only=True,
            sucess=False
        ),
        Test(
            "Sintaxe error after str",
            code='print: "HELLO" error',
            compile_only=True,
            sucess=False
        ),
        Test(
            "Sintaxe error after char",
            code="print: 'A' error",
            compile_only=True,
            sucess=False
        ),
        Test(
            "Unclosed block",
            code="""
                if True{;
                    print: "ERROR";
            """,
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
        ),
        Test(
            "Input test",
            code=".i = input:;print: .i;",
            compile_output="0400: 20 0D 04 8D 00 03 AD 00 03 20 EF FF 00 AD 11 D0 10 FB AD 10 D0 29 7F 60 ",
            compile_only=True,
        ),
        Test(
            "If test",
            code="""
                if True{;
                    print: "IF TEST";
                }
                else{;
                    print: "ERROR";
                }

                .a = True == False;
                if .a{;
                    print: "ERROR";
                } elif .a == False{;
                    print: "ELIF TEST";
                }

                .b = 10;
                if .b == 9{;
                    print: "ERROR";
                } elif .b == 11{;
                    print: "ERROR";
                }
                else{;
                    print: "ELSE TEST";
                }
            """,
            output="IF TESTELIF TESTELSE TEST"
        ),
    Test(
        "while test",
        code="""
            while True{;
                print: "TEST WHILE";
                break;
            }
            .a = True;
            while .a{;
                print: "TEST WHILE 2";
                .a = False;
            }
        """,
        output="TEST WHILETEST WHILE 2"
    ),
    Test(
        "string test",
        code="""
            ~a = "STRING";
            print: ~a;

            if ~a == "STRING"{;
                print: "OK";
            }

            ~b = "STRING2";
            if ~a == ~b{;
                print: "ERROR";
            }
            else{;
                print: "OK2";
            }

            ~c = "ABC";

            print: ~c[0];

            .d = 1;
            print: ~c[.d];

            ~c[0] = '@';

            print: ~c;
        """,
        output="STRINGOKOK2AB@BC"
    ),
    Test(
        "quit test",
        code="""
            print: "OK";
            quit:;
            print: 'E';
        """,
        output="OK"   
    )
    ]

    math_test = [
        # addition test ---
        Test(
            "Simple addition test",
            code="print: 65+1;",
            output="B"
        ),
        Test(
            "char addition test",
            code="print: 'A'+1;print: '!' + '#';",
            output="BD"
        ),
        # substraction test ---
        Test(
            "Simple substraction test",
            code="print: 65-1;",
            output="@"
        ),
        Test(
            "char substraction test",
            code="print: 'A'-1;",
            output="@"
        ),
        # multiplication test ---
        Test(
            "Simple multiplication test",
            code="print: 13*5;", # 13 * 5 = 65 'A'
            output="A"
        ),
        Test(
            "char multiplication test",
            code="print: '!'*2;", # 33 * 2 = 66 'B'
            output="B"
        ),
        # division test ---
        Test(
            "Simple division test",
            code="print: 130/2;", # 130 / 2 = 65 'A'
            output="A"
        ),
        Test(
            "char division test",
            code="print: 'Z'/2;", # 90 / 2 = 45 '-'
            output="-"
        ),
        # advenced test ---
        Test(
            "Different operation test", # warning: smart do operation in order, not priority
            code="""
                print: 65+3-2/2;
                print: 80+3-2/4*3;
            """,
            output="!<"
        ),
        Test(
            "Math operation with variable",
            code="""
                .a = 1;
                .b = 2;
                .c = 3;
                .d = 10;
                .e = 'A';

                print: .a + 'A';
                print: .b + 'A';
                print: 'A' - .c;
                print: .e + .a;
                print: .c * .d + .d;
                .x = .d / .b;
                print: .x + .e;
            """,
            output="BC>B(F"
        )
    ]

    runtime_error_test = [
        Test(
            "Error keyword test",
            code="""
                print: "OK";
                error 'A';
                print: "KO";
            """,
            output="OKEA"
        ),
        Test(
            "Error keyword with variable",
            code="""
                .code_e = 'B';
                error .code_e;
                print: "KO";
            """,
            output="EB"
        ),
        Test(
            "Division by zero test",
            code="""
                .a = 1;
                .b = 0;
                .c = .a / .b;
                print: "KO";
            """,
            output="E/"
        ),
        Test(
            "Index error test",
            code="""
                .index = 30;
                ~str = "TEST";
                print: ~str[.index];
            """,
            output="EI"    
        )
    ]

    global_tests = syntaxe_error_test + tests + math_test + runtime_error_test

    try:
        for test in global_tests:
            test.run()
    except StopTest as st:
        print(f"{Colors.BG_YELLOW}{st}{Colors.RESET}")

    if all_ok:
        print(f"{Colors.BG_GREEN}All tests without error!{Colors.RESET}")
    else:
        print(
            f"{Colors.BG_RED}Some tests failed!{Colors.RESET}",
            f"{Colors.RED}Error: {error_counter}/{len(global_tests)}{Colors.RESET}",
        )
    
except KeyboardInterrupt:
    print(f"\n{Colors.BG_YELLOW}Test stopped by user\nKeyboard interrupt.{Colors.RESET}")

except Exception as e:
    print(f"{Colors.BG_RED}An error occured during test: {e}{Colors.RESET}")