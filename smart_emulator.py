
from sys import argv
import tkinter as tk
from tkinter import scrolledtext, messagebox

from threading import Thread

from smart_compiller import compile_smarty

if len(argv) != 2:
    messagebox.showerror("Error", "Bad arg, need file name.")

code = compile_smarty(file=argv[1], argv=[], START_ADRESSE="0400: ", CODE_ADRESSE=1024, make_file=False)

window_emulator = tk.Tk()
window_emulator.title("Smart emulator")

monitor = scrolledtext.ScrolledText(window_emulator, height=10, width=20, bg="#000000", fg="#0099FF")
monitor.pack()

frame_option = tk.Frame(window_emulator)
frame_option.pack()

def see_RAM() -> None:
    """Open a window for see the ram."""
    def update_RAM() -> None:
        """Update the text for RAM"""
        RAM_info.delete(0.0, tk.END)
        RAM_info.insert(0.0, str(RAM))

        window_RAM.after(100, update_RAM)

    window_RAM = tk.Toplevel(window_emulator)
    window_RAM.title("RAM")

    RAM_info = tk.Text(window_RAM)
    RAM_info.pack()

    update_RAM()


button_RAM = tk.Button(frame_option, text="See RAM", command=see_RAM)
button_RAM.grid(column=0, row=0)

RAM = {}

def run_smart() -> None:
    """Run smart code."""
    global code, RAM

    code = code.split(" ")

    START = int(code[0][:-1], base=16)

    run_step = 1

    accumulator = {"A":"00", "X":"00", "Y":"00"}

    RAM = {"0" + hex(i)[2:]:"00" for i in range(0x300, 0x400 + 1)}

    carry_flag = False

    while run_step < len(code):
        run = code[run_step]

        if run == "A9":     # A
            accumulator["A"] = code[run_step + 1]
            run_step += 2
        
        elif run == "A2":
            accumulator["X"] = code[run_step + 1]
            run_step += 2
        
        elif run == "A0":
            accumulator["Y"] = code[run_step + 1]
            run_step += 2
        
        elif run == "8D":
            RAM[code[run_step + 2] + code[run_step + 1]] = accumulator["A"]

            run_step += 3

        elif run == "AD":
            accumulator["A"] = RAM[code[run_step + 2] + code[run_step + 1]]

            run_step += 3
        
        elif run == "20":
            run_step += 1

            code[run_step]

            if code[run_step] == "EF" and code[run_step + 1] == "FF":
                monitor.insert(tk.END, chr(int(accumulator["A"], base=16)))

                run_step += 2
        
        elif run == "00":
            break

        elif run == "4C":   # goto
            goto = code[run_step + 2] + code[run_step + 1]

            run_step = int(goto, base=16) - START + 1
        
        elif run == "18":
            carry_flag = False

            run_step += 1
        
        elif run == "69":       # add to A
            add = code[run_step + 1]

            new_A = int(accumulator["A"], base=16) + int(add, base=16)

            if new_A >= 256:
                carry_flag = True

                new_A -= 256

            accumulator["A"] = hex(new_A)[2:]

            run_step += 2
        
        elif run == "6D":
            RAM_adress = code[run_step + 2] + code[run_step + 1]
            

            add = RAM[RAM_adress]

            new_A = int(accumulator["A"], base=16) + int(add, base=16)

            if new_A >= 256:
                carry_flag = True

                new_A -= 256

            accumulator["A"] = hex(new_A)[2:]

            run_step += 3
        
        else:
            messagebox.showerror("Error", f"Unknow assembly : {run}, at {run_step} step.")
            break
    
    monitor.insert(tk.END, "\n\nEnd of run")
   


thread_run = Thread(target=run_smart, daemon=True)
thread_run.start()


window_emulator.mainloop()
