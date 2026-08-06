"""
This programme is for test all functionalities of smart.
"""
import os
import traceback
import threading
import time
import sys
import logging

if "--compile-debug" in sys.argv:
    sys.argv.remove("--compile-debug")

    logging.basicConfig(
        format="SmartCompiller %(levelname)s: %(message)s",
        level=logging.INFO,
        stream=sys.stdout,  # for redirecting the output
        force=True
    )
else:
    logging.basicConfig(
        format="SmartCompiller %(levelname)s: %(message)s",
        level=logging.WARNING,
        stream=sys.stdout,
        force=True
    )

import smart_emulator
from smart_compiller import compile_smarty
from compiller_tool import compiller_data_run
from compiller_tool.color_tool import Colors
from compiller_tool.smart_exception import SmartError


ERASE_PROGRESSBAR = "\033[2K\033[1G"

SYMBOL_OK = False

TEST_OK = "✔️   " if SYMBOL_OK else f"{Colors.GREEN}OK{Colors.RESET}  "
TEST_ERROR = "❌   " if SYMBOL_OK else f"{Colors.RED}ERR{Colors.RESET}  "

class TestError(Exception):
    """Main Exception for test."""
    pass

class StopTest(TestError):
    """This exception is for stop the test."""
    pass

class OutputError(TestError):
    """If the output of programme are not good."""
    pass

class TimeOut:
    """For the time out on test. Help full on while or goto."""
    def __init__(self, timeout:int):
        """Start the timeout, with a `timeout` in second.
        raise a TimeoutError if time is out."""
        self.timeout = timeout

        self.actual_time = 0
        self.end = False

        self.timer = threading.Thread(target=self.control_time, daemon=True)
        self.timer.start()
        
    def control_time(self):
        """Check if the time is out."""
        while not self.end:
            if self.actual_time >= self.timeout:
                time_out_error = f"{Colors.RED}Time out on test. Test take too long : have {self.timeout}s max but use {self.actual_time}s.{Colors.RESET}"

                input(f"{time_out_error}\n{Colors.BG_YELLOW}Need to stop test... Press enter or Ctrl+C for quit...")

                sys.exit(1)

                #raise TimeoutError(time_out_error)
            self.actual_time += 1

            time.sleep(1)

class Test:
    """This class is for testing all functionalities of smart."""
    def __init__(self, name:str, code:str, output:str="", compile_output:str="", compile_only:bool=False, sucess:bool=True, timeout:int=-1):
        """
        timeout : if -1 no time out, else time out in second.
        """
        self.name = name
        self.code = code
        self.compile_only = compile_only
        self.output = output + "\n\nEnd of run"
        self.compile_output = compile_output
        self.sucess = sucess
        self.timeout = timeout
    
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

        compiller_data_run.reset_data()

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
                #else:
                #    print(f"{Colors.YELLOW}Warning: hex compilation of Smart programme is not normal{Colors.RESET}")

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
                    if self.timeout != -1:
                        time_out = TimeOut(self.timeout)
                    output = smart_emulator.start_test(self.code_compile)

                    if self.timeout != -1:
                        time_out.end = True

                    if output != self.output:
                        raise OutputError(f"The output of programme is not good:\n{output}")

                except TimeoutError as e:
                    print(str(e))

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
                f"{ERASE_PROGRESSBAR}{TEST_ERROR}{Colors.BG_RED}ERROR: Test failed{Colors.RESET}",
                f"{Colors.RED}{'Compilation error' if compilation_error else 'Runtime error'}",
                f"Error output: {error_output}{Colors.RESET}",

                sep="\n"
            )

            reply = input("Continue test ? (y/n): ")

            if reply.lower() == "n":
                raise StopTest("Test stopped by user")
        
            print(end="\n"*10)
        
        else:
            
            print(f"{ERASE_PROGRESSBAR}{TEST_OK}{Colors.BG_GREEN}Test OK{Colors.RESET}", end="\n"*10)

class ModuleTest(Test):
    """This class is for testing a Smart code with some modules (in different files)."""
    def __init__(self, name:str, code_modules:list[tuple[str, str]], output:str="", compile_output:str="", compile_only:bool=False, sucess:bool=True):
        super().__init__(name, code_modules[0][1], output, compile_output, compile_only, sucess)

        self.code_modules = code_modules[1:]    # get all module excepted main module

    '''def show_module_test(self) -> None:
        """Print the detail of module test"""
        print(f"{Colors.BG_BLUE}Test with some modules:{Colors.RESET}")
        self.show_test()'''

    def run_modules(self) -> None:
        """This function make all module and run test.
        Next dellet the modules."""

        for module in self.code_modules:
            with open(f"test/{module[0]}", "w") as f:
                f.write(module[1])
        
        self.run()

        for module in self.code_modules:
            os.remove(f"test/{module[0]}")

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

    boolean_test = [
        Test(
            "Simple boolean",
            code="""
                .a = True;
                .b = False;

                print: .a + '0';
                print: .b + '0';

                print: True + '0';
                print: False + '0';
            """,
            output="1010"
        ),
        Test(
            "Boolean comparaison",
            code="""
                .a = True;
                .b = False;

                .comparaison1 = .a == .b;
                print: .comparaison1 + '0';

                .comparaison2 = .a == True;
                print: .comparaison2 + '0';

                .comparaison3 = .b == False;
                print: .comparaison3 + '0';

                .comparaison4 = True == 1;
                print: .comparaison4 + '0';

                .comparaison5 = False == 0;
                print: .comparaison5 + '0';

                .comparaison6 = True == False;
                print: .comparaison6 + '0';
            """,
            output="011110"
        ),
        Test(
            "Boolean if",
            code="""
                .a = True;
                if .a{;
                    print: "IF TEST";
                }
                else{;
                    print: "ERROR";
                }
            """,
            output="IF TEST"
        )
    ]

    test_int_hex = [
        Test(
            "Simple int and hex",
            code="""
                .a = 65;
                .b = 0x41;

                print: .a;
                print: .b;
            """,
            output="AA"
        ),
        # ---- test error ----
        Test(
            "Value too big (int)",
            code=".a = 300;",
            sucess=False
        ),
        Test(
            "Value too big (hex)",
            code=".a = 0x300;",
            sucess=False
        ),
        Test(
            "Bad hex value",
            code=".a = 0xG;",
            sucess=False
        )
    ]

    test_char = [
        Test(
            "Simple char",
            code="print: 'A';",
            output="A"
        ),
        Test(
            "Char in variables",
            code="""
                .a = 'A';
                print: .a;
                
                .b = 'B';
                print: .b;
            """,
            output="AB"
        ),
        # ----- error 
        Test(
            "Char not autorize",
            code=".a = 'a'",
            sucess=False
        ),
        Test(
            "Bad len char",
            code=".a = 'AA'",
            sucess=False
        )
    ]

    advenced_value_test = [
        Test(
            "Simple str",
            code="""
                ~a = "STRING";
                print: ~a;

                print: "STRING2";
            """,
            output="STRINGSTRING2"
        ),
        Test(
            "Simple list",
            code="""
                ~a = ['A', 'B', 'C'];
                print: ~a;

                print: ['1', '2', '3'];
            """,
            output="ABC123"
        ),
        Test(
            "F-string test",
            code="""
                ~str1 = F"AA{65}AA{'@'}";
                print: ~str1;

                .a = 'A';
                .b = '1';
                .c = 64;

                ~str2 = F"NEW FSTR{.a}{.b}{.c}";
                print: ~str2;
                """,
            output="AAAAA@NEW FSTRA1@"
        ),
        Test(
            "List with var",
            code="""
                .a = 'A';
                .b = 'B';
                .c = 'C';

                ~list1 = [.a, .b, .c];
                print: ~list1;

                ~list2 = [.a, '1', .b, '2', .c, '3'];
                print: ~list2;
            """,
            output="ABCA1B2C3"
        ),
        Test(
            "Index on str",
            code="""
                ~str1 = "STRING";
                print: ~str1[0];
                print: ~str1[3];

                print: ~str1[-16];

                .a = 1;
                print: ~str1[.a];
            """,
            output="SIGT"
        ),
        Test(
            "Index on list",
            code="""
                ~list1 = ['A', 'B', 'C'];
                print: ~list1[0];
                print: ~list1[2];

                .a = 1;
                print: ~list1[.a];

                print: ~list1[-19];
            """,
            output="ACBC"
        ),
        Test(
            "Str an list comparison",
            code="""
                ~str1 = "STRING";
                ~list1 = ['S', 'T', 'R', 'I', 'N', 'G'];
                print: ~str1 == ~list1;"""
        ),
        # ---- error ----
        Test(
            "Str not in advenced var",
            code='.a = "STRING";',
            sucess=False
        ),
        Test(
            "Simple value in advenced var",
            code="~a = 1;",
            sucess=False
        )
    ]

    register_tests = [
        Test(
            "Accumulator A test",
            code="""
                A = 65;
                print: A;

                A = '0';
                print: A;
            """,
            output="A0"
        ),
        Test(
            "Register X and Y test",    # this test can't have output because X and Y are not printable
            code="""
                X = 1;
                Y = 2;
            """,
            output=""
        ),
        # ---- error ----
        Test(
            "Print X test",
            code="print: X;",
            sucess=False
        ),
        Test(
            "Print Y test",
            code="print: Y;",
            sucess=False
        ),
        Test(
            "Set advanced var on A",
            code='A = "STR";',
            sucess=False
        ),
        Test(
            "Set advanced var on X",
            code='X = "STR";',
            sucess=False
        ),
        Test(
            "Set advanced var on Y",
            code='Y = "STR";',
            sucess=False
        )
    ]

    goto_test = [
        Test(
            "Goto test 1",
            code="""
                goto: label1;
                print: "ERROR";
                #label1;
                print: "GOTO TEST 1";
            """,
            output="GOTO TEST 1"
        ),
        Test(
            "Advenced Goto test",
            code="""
                goto: label;

                // this code are succeptible to move adress
                if True{;
                    print: "ERROR";
                }
                else {;
                    A = 65;
                }

                while False{;
                    print: 'E';
                }
                
                #label;    
                print: "GOTO TEST 2";        
            """,
            output="GOTO TEST 2"
        ),
        # ---- error ----
        Test(
            "Goto label not found",
            code="""
                goto: label_not_found;
                print: "ERROR";
            """,
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

    if_test = [
        Test(
            "Simple if test",
            code="""
                .a = True;
                if .a{;
                    print: "OK";
                }

                if True{;
                    print: "OK2";
                }

                .b = False;
                if .b{;
                    print: "ERROR";
                }

                if False{;
                    print: "ERROR2";
                }
            """,
            output="OKOK2"
        ),
        Test(
            "Condition test",
            code="""
                .a = True;
                if .a == True{;
                    print: "OK";
                }

                if .a == False{;
                    print: "ERROR";
                }

                .b = 'A';

                if .b == 'A'{;
                    print: "OK2";
                }
                if .b == 'B'{;
                    print: "ERROR2";
                }
            """,
            output="OKOK2"
        ),
        Test(
            "Else test",
            code="""
                .a = False;
                if .a{;
                    print: "ERROR";
                }
                else{;
                    print: "OK";
                }

                .b = True;
                if .b{;
                    print: "OK2";
                }
                else{;
                    print: "ERROR2";
                }
            """,
            output="OKOK2",
        ),
        Test(
            "Elif test",
            code="""
                .a = False;
                .b = True;

                if .a{;
                    print: "ERROR";
                }
                elif .b{;
                    print: "OK";
                }
                else{;
                    print: "ERROR2";
                }

                if False{;
                    print: "ERROR3";
                }
                elif False{;
                    print: "ERROR4";
                }
                elif True{;
                    print: "OK2";
                }
                else{;
                    print: "ERROR5";
                }
            """,
            output="OKOK2"
        ),
        Test(
            "Advenced structure condition",
            code="""
                .a = True;
                .b = False;    
            
                if True{;
                    print: "OK";

                    if .a{;
                        print: "OK2";

                        if .b{;
                            print: "ERROR";
                        }
                        else{;
                            print: "OK3";

                            if False{;
                                print: "ERROR2";
                            }
                            elif False{;
                                print: "ERROR3";
                            }
                            else{;
                                print: "OK4";
                            }
                        }
                    }
                    else{;
                        print: "ERROR";
                    }
                }
            """,
            output="OKOK2OK3OK4"
        ),
        # ---- error ----
        Test(
            "Else without if",
            code="""
                else{;
                    print: "ERROR";
                }
            """,
            sucess=False
        ),
        Test(
            "Elif without if",
            code="""
                elif True{;
                    print: "ERROR";
                }
            """,
            sucess=False
        )
    ]

    while_test = [      # warning in this test, because while can be infinite...
        #Test(
        #    "While True",
        #    code="""
        #        while True{;
        #            print: 'A';
        #        }
        #    """,
        #    timeout=2
        #),
        Test(
            "Simple while test",
            code="""
                .i = 0;
                .loop = True;
                while .loop {;
                    .i = .i + 1;
                    if .i == 5{;
                        .loop = False;
                    }
                    print: '0' + .i;    
                }
            """,
            output="12345",
            timeout=5
        ),
        Test(
            "Break in while",
            code="""
                while True{;
                    print: "TEST";
                    break;
                }
            """,
            output="TEST",
            timeout=5
        ),
        Test(
            "Continue in while",
            code="""
                .a = True;

                while .a{;
                    .a = False;
                    print: "TEST1";
                    continue;
                    print: "ERROR";
                }
            """,
            output="TEST1",
            timeout=5
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

    modules_test = [
        ModuleTest(
            "Simple module test",
            code_modules=[
                (
                    "test.sma",
                    'import "test/module1.sma";'
                ),
                (
                    "module1.sma",
                    'print: "MODULE TEST";'
                )
            ],
            output="MODULE TEST"
        ),
        ModuleTest(
            "Get function and var from module",
            code_modules=[
                (
                    "test.sma",
                    """
                    import "test/module2.sma";

                    function:;
                    print: .var1;
                    print: ~var2;

                    print: "OK";
                    """
                ),
                (
                    "module2.sma",
                    """
                    void function{;
                        print: "FUNCTION TEST";
                    }
                    
                    .var1 = 'A';
                    ~var2 = "STRING";
                    """
                )
            ],
            output="FUNCTION TESTASTRINGOK"
        ),
        ModuleTest(
            "Recursive import",
            code_modules=[
                (
                    "test.sma",
                    """
                    import "test/module1.sma";

                    print: .var1;
                    print: .var2;
                    func:;
                    """
                ),
                (
                    "module1.sma",
                    """
                    import "test/module2.sma";

                    .var1 = 'A';
                    """
                ),
                (
                    "module2.sma",
                    """
                    .var2 = 'B';

                    void func{;
                        print: "MODULE2";
                    }
                    """
                ),
            ],
            output="ABMODULE2"
        ),
        # test error with modules:
        ModuleTest(
            "Module not found test",
            code_modules=[
                (
                    "test.sma",
                    'import "test/module_not_found.sma";'
                )
            ],
            sucess=False
        ),
        ModuleTest(
            "Module with error",
            code_modules=[
                (
                    "test.sma",
                    'import "test/module_error.sma";'
                ),
                (
                    "module_error.sma",
                    'print: "ERROR' # error sintaxe the the error
                )
            ],
            sucess=False
        )

        #ModuleTest(    # uncomment for set the test. But this test have a long output
        #    "Self import test",
        #    code_modules=[
        #        (
        #            "test.sma",
        #            'import "test/test.sma";'
        #        )
        #    ],
        #    sucess=False
        #)
    ]

    built_in = [
        Test(
            "asm_entry test",
            code="""
                asm_entry: "A9 41 20 EF FF";  // print 'A'
                asm_entry: "A9 42 20 EF FF";  // print 'B'

                print: "OK";
            """,
            output="ABOK"
        ),
        Test(
            "quit function test",
            code="""
                print: "OK";
                quit:;
                print: "ERROR";
            """,
            output="OK"
        ),
        Test(
            "wozm test",
            code="""
                print: "OK";
                wozm:;
                print: "ERROR";
            """,
            output="OK"
        ),
        # --- error ---
        Test(
            "Bad hex on asm_entry",
            code='asm_entry: "A9 41 20 EF FG";',
            sucess=False
        ),
        Test(
            "Bad arg on quit",
            code="quit: 'A';",
            sucess=False
        ),
        Test(
            "Bad arg on wozm",
            code="wozm: 'A';",
            sucess=False
        ),
        Test(
            "Bad arg on input",
            code=".a = input: 'A';",
            sucess=False,
            compile_only=True
        )
    ]

    global_tests = syntaxe_error_test + tests + math_test + runtime_error_test + modules_test + boolean_test + test_int_hex + test_char + advenced_value_test + register_tests + goto_test + if_test + while_test

    try:
        for test in global_tests:
            if isinstance(test, ModuleTest):
                test.run_modules()
            else:
                test.run()
    except StopTest as st:
        print(f"{Colors.BG_YELLOW}{st}{Colors.RESET}")

    if all_ok:
        print(f"{TEST_OK}{Colors.BG_GREEN}All tests without error!{Colors.RESET}")
    else:
        print(
            f"{TEST_ERROR}{Colors.BG_RED}Some tests failed!{Colors.RESET}",
            f"{Colors.RED}Error: {error_counter}/{len(global_tests)}{Colors.RESET}",
        )
    
except KeyboardInterrupt:
    print(f"\n{Colors.BG_YELLOW}Test stopped by user\nKeyboard interrupt.{Colors.RESET}")

except Exception as e:
    print(
        f"{Colors.BG_RED}An error occured during test: {e}{Colors.RESET}",
        traceback.format_exc(),
        sep="\n"
    )