
from sys import argv
import tkinter as tk
from tkinter import scrolledtext, messagebox
from time import sleep

from threading import Thread

from smart_compiller import compile_smarty

if len(argv) != 2:
    messagebox.showerror("Error", "Bad arg, need file name.")

code = compile_smarty(file=argv[1], argv=[], START_ADRESSE="0400: ", CODE_ADRESSE=1024, make_file=False)

window_emulator = tk.Tk()
window_emulator.title("Smart emulator")

monitor = scrolledtext.ScrolledText(window_emulator, height=10, width=20, bg="#000000", fg="#0099FF")
monitor.pack()

def disable_edit(event:tk.Event) -> str:
    return "break"

monitor.bind("<Key>", disable_edit)

frame_option = tk.Frame(window_emulator)
frame_option.pack()

def print_on_text(text:str) -> None:
    """Insert on the scolledtext the text."""
    monitor.insert(tk.END, text)
    monitor.see(tk.END)


def see_memory() -> None:
    """Open a window for see the memory (RAM, accumulator, carry_flag)."""
    def update_memory() -> None:
        """Update the listbox for memory"""
        # RAM
        RAM_info.delete(0, tk.END)

        new_ram = (f"{adress}       {RAM[adress]}" for adress in RAM)

        RAM_info.insert(0, "Adress    Value")

        for adress in new_ram:
            RAM_info.insert(tk.END, adress)
        
        # accumulator

        accumulator_info.delete(0, tk.END)
        
        for ac in ("ACCUMULATOR    Value", f"A     {accumulator["A"]}", f"X     {accumulator["X"]}", f"Y     {accumulator["Y"]}"):
            accumulator_info.insert(tk.END, ac)

        # carry flag

        text_carry_str.set(f"Carry Flag : {int(carry_flag)}")

        window_memory.after(100, update_memory)

    window_memory = tk.Toplevel(window_emulator)
    window_memory.title("Memory")

    frame_RAM = tk.LabelFrame(window_memory, text="RAM")

    RAM_info = tk.Listbox(frame_RAM)
    RAM_info.pack()

    frame_RAM.grid(column=0, row=0)

    frame_accumulator = tk.LabelFrame(window_memory, text="Accumulator (register)")

    accumulator_info = tk.Listbox(frame_accumulator)
    accumulator_info.pack()

    frame_accumulator.grid(column=1, row=0)

    carry_frame = tk.LabelFrame(window_memory, text="Carry Flag")

    text_carry_str = tk.StringVar(carry_frame)

    text_carry = tk.Label(carry_frame, textvariable=text_carry_str)
    text_carry.pack()

    carry_frame.grid(column=0, row=1)


    update_memory()


button_RAM = tk.Button(frame_option, text="See memory", command=see_memory)
button_RAM.grid(column=0, row=0)

normal_speed = True

def emulator_setting() -> None:
    """Open a window for the setting of emulator"""
    def close_setting() -> None:
        """Destroy the window and set setting."""
        global normal_speed
        normal_speed = var_speed.get()
        
        window_setting.destroy()

    window_setting = tk.Toplevel(window_emulator)
    window_setting.title("Emulator settings")

    var_speed = tk.BooleanVar(window_setting, value=normal_speed)

    chek_speed = tk.Checkbutton(window_setting, text="Run with a speed of 1Mhz\n(speed of MOS 8502)", variable=var_speed)
    chek_speed.pack()

    button_validate = tk.Button(window_setting, text="Validate", command=close_setting)
    button_validate.pack()


button_setting = tk.Button(frame_option, text="Setting", command=emulator_setting)
button_setting.grid(column=1, row=0)

RAM = {}
accumulator = {}
carry_flag = False

def run_smart() -> None:
    """Run smart code."""
    global code, RAM, accumulator, carry_flag

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
                print_on_text(chr(int(accumulator["A"], base=16)))

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

        if normal_speed:
            sleep(0.01)
    
    print_on_text("\n\nEnd of run")
   


thread_run = Thread(target=run_smart, daemon=True)
thread_run.start()


window_emulator.mainloop()
