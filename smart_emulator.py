# -*- coding: utf-8 -*-

"""
A Smart emulator.
Run Smart code one a emulator.
"""


from sys import argv
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from time import sleep
from pathlib import Path
import json

from threading import Thread

from smart_compiller import compile_smarty

if len(argv) != 2:
    messagebox.showerror("Error", "Bad arg, need file name.")
    quit()

if argv[1] == "--asm-entry":
    code = input("Enter the assembly code : ")#.split(" ")
else:
    code = compile_smarty(file=argv[1], argv=[], START_ADRESSE="0400: ", CODE_ADRESSE=1024, make_file=False)

asm_code = code

window_emulator = tk.Tk()
window_emulator.title("Smart emulator")

monitor = scrolledtext.ScrolledText(window_emulator, height=24, width=39, bg="#000000", fg="#0099FF", insertwidth=10, insertbackground="#B1B1B1", insertofftime=0)
monitor.pack()
monitor.focus_force()

def disable_edit(event:tk.Event) -> str:
    return "break"

monitor.bind("<Key>", disable_edit)

frame_option = tk.Frame(window_emulator)
frame_option.pack()

ALLOW_CHAR = "!\"#$%'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_\n "

def print_on_text(text:str, sys_message:bool=False) -> None:
    """Insert on the scolledtext the text."""
    if not sys_message:
        text = text.upper()
        if text not in ALLOW_CHAR:      # forbiden char
            return

    monitor.insert(tk.END, text)
    monitor.see(tk.END)


def see_memory() -> None:
    """Open a window for see the memory (RAM, accumulator, carry_flag)."""
    def update_memory() -> None:
        """Update the listbox for memory"""
        # RAM
        pos_listbox = RAM_info.yview()[0]

        RAM_info.delete(0, tk.END)

        new_ram = (f"{adress}       {RAM[adress]}" for adress in RAM)

        RAM_info.insert(0, "Adress    Value")

        for adress in new_ram:
            RAM_info.insert(tk.END, adress)
        
        RAM_info.yview_moveto(pos_listbox)
        
        # accumulator

        accumulator_info.delete(0, tk.END)
        
        for ac in ("ACCUMULATOR    Value", f"A     " + accumulator["A"], f"X     " + accumulator["X"], f"Y     " + accumulator["Y"]):
            accumulator_info.insert(tk.END, ac)

        # carry flag

        text_carry_str.set(f"Carry Flag : {carry_flag}")

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

def window_code() -> None:
    """Open a window for see the code and see the step."""
    def update_code() -> None:
        """Update the listbox for code"""
        pos_listbox = list_code.yview()[0]

        list_code.delete(0, tk.END)

        adress_conter = 0

        list_code.insert(0, "Adress    Code")

        for i in code[1:]:
            list_code.insert(tk.END, f"{hex(0x400 + adress_conter)}      {i}")
            adress_conter += 1
        
        list_code.yview_moveto(pos_listbox)

        list_code.itemconfig(run_step, {'bg':'#0099FF', 'fg':'#000000'})

        window_code.after(100, update_code)

    window_code = tk.Toplevel(window_emulator)
    window_code.title("See code")

    list_code = tk.Listbox(window_code, width=50)
    list_code.pack(expand=True, fill=tk.BOTH)
    update_code()

button_code = tk.Button(frame_option, text="See code", command=window_code)
button_code.grid(column=1, row=0)

normal_speed = "1Mhz"

def emulator_setting() -> None:
    """Open a window for the setting of emulator"""
    def close_setting() -> None:
        """Destroy the window and set setting."""
        global normal_speed
        normal_speed = var_speed.get()
        
        window_setting.destroy()

    window_setting = tk.Toplevel(window_emulator)
    window_setting.title("Emulator settings")

    var_speed = tk.StringVar(window_setting, value=normal_speed)

    radio_speed_mos = tk.Radiobutton(window_setting, text="Run with a speed of 1Mhz\n(speed of MOS 8502)", variable=var_speed, value="1Mhz")
    radio_speed_mos.pack()

    radio_debug = tk.Radiobutton(window_setting, text="Run for debug", variable=var_speed, value="Debug")
    radio_debug.pack()

    radio_normal = tk.Radiobutton(window_setting, text="Run with max speed", variable=var_speed, value="Normal")
    radio_normal.pack()

    button_validate = tk.Button(window_setting, text="Validate", command=close_setting)
    button_validate.pack()


button_setting = tk.Button(frame_option, text="Setting", command=emulator_setting)
button_setting.grid(column=2, row=0)

RAM = {}
accumulator = {}
carry_flag = 0
run_step = 0


def run_smart() -> None:
    """Run smart code."""
    global code, RAM, accumulator, carry_flag, run_step

    code = code.split(" ")

    while code[-1] == "":
        del code[-1]

    START = int(code[0][:-1], base=16)

    run_step = 1

    accumulator = {"A":"00", "X":"00", "Y":"00"}

    RAM = {"0" + hex(i)[2:]:"00" for i in range(0x300, 0x400 + 1)}

    carry_flag = 0

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
            adress = code[run_step + 2] + code[run_step + 1]

            if 0x300 <= int(adress, base=16) >= 0x400:    # write one the programme
                try:
                    code[int(adress, base=16) - START + 1] = accumulator["A"]
                except:
                    messagebox.showerror("Error", "Write on unknow adress.", detail="Detail: {}".format(hex(0x400 + int(adress, base=16) - START + 1)).upper())
                    break
            else:
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
            
            else:
                messagebox.showerror("Error", "Unknow adress for call.")
                break
        
        elif run == "00":
            break

        elif run == "4C":   # goto
            goto = code[run_step + 2] + code[run_step + 1]

            run_step = int(goto, base=16) - START + 1
        
        elif run == "18":
            carry_flag = 0

            run_step += 1
        
        elif run == "69":       # add to A
            add = code[run_step + 1]

            new_A = int(accumulator["A"], base=16) + int(add, base=16)

            if new_A >= 256:
                carry_flag = 1

                new_A -= 256

            accumulator["A"] = hex(new_A)[2:]

            run_step += 2
        
        elif run == "6D":
            RAM_adress = code[run_step + 2] + code[run_step + 1]
            

            add = RAM[RAM_adress]

            new_A = int(accumulator["A"], base=16) + int(add, base=16)

            if new_A >= 256:
                carry_flag = 1

                new_A -= 256

            accumulator["A"] = hex(new_A)[2:]

            run_step += 3
        
        else:
            messagebox.showerror("Error", f"Unknow assembly : {run}, at {run_step} step.")
            break

        if normal_speed == "1Mhz":
            sleep(0.0025)
        elif normal_speed == "Debug":
            sleep(1.5)
        
    
    print_on_text("\n\nEnd of run")
   
menu_window = tk.Menu(window_emulator)
window_emulator.config(menu=menu_window)

menu_save = tk.Menu(menu_window, tearoff=0)
menu_window.add_cascade(label="Save...", menu=menu_save)

def save_monitor() -> None:
    """Save the text of monitor in a *.txt file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if file_path:
        Path(file_path).write_text(monitor.get("1.0", tk.END), encoding="utf-8")

menu_save.add_command(label="Save monitor (as *.txt)", command=save_monitor)

def export_memory() -> None:
    """Export RAM, accumulator and carry flag in a *.json file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Json files", "*.json")])

    if file_path:
        data = {"RAM": RAM, "accumulator": accumulator, "carry_flag": carry_flag}

        Path(file_path).write_text(json.dumps(data, indent=4), encoding="utf-8")

menu_save.add_command(label="Save memory (as *.json)", command=export_memory)

def save_asm() -> None:
    """Save the assembly code in a *.asm file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".asm", filetypes=[("Assembly files", "*.asm")])

    if file_path:
        Path(file_path).write_text(asm_code, encoding="utf-8")

menu_save.add_command(label="Save assembly (as *.asm)", command=save_asm)

thread_run = Thread(target=run_smart, daemon=True)
thread_run.start()


window_emulator.mainloop()
