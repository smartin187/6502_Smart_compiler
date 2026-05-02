code = input()

import tkinter as tk
from tkinter import scrolledtext

from threading import Thread

window_emulator = tk.Tk()
window_emulator.title("Smart emulator")

monitor = scrolledtext.ScrolledText(window_emulator)
monitor.pack()

def run_smart() -> None:
    """Run smart code."""
    global code

    code = code.split(" ")

    run_step = 1

    ACCUMULATOR = {"A":"00", "X":"00", "Y":"00"}

    RAM = {"0" + hex(i)[2:]:"00" for i in range(0x300, 0x400 + 1)}


    while run_step < len(code):
        run = code[run_step]

        if run == "A9":     # A
            ACCUMULATOR["A"] = code[run_step + 1]
            run_step += 2
        
        elif run == "A2":
            ACCUMULATOR["X"] = code[run_step + 1]
            run_step += 2
        
        elif run == "A0":
            ACCUMULATOR["Y"] = code[run_step + 1]
            run_step += 2
        
        elif run == "8D":
            RAM[code[run_step + 2] + code[run_step + 1]] = ACCUMULATOR["A"]

            run_step += 3

        elif run == "AD":
            ACCUMULATOR["A"] = RAM[code[run_step + 2] + code[run_step + 1]]

            run_step += 3
        
        elif run == "20":
            run_step += 1

            code[run_step]

            if code[run_step] == "EF" and code[run_step + 1] == "FF":
                monitor.insert(tk.END, chr(int(ACCUMULATOR["A"], base=16)))

                run_step += 2
        
        elif run == "00":
            break

        print(run)

       
    
    monitor.insert(tk.END, "\n\nEnd of run")
   


thread_run = Thread(target=run_smart, daemon=True)
thread_run.start()


window_emulator.mainloop()
