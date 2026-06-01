# -*- coding: utf-8 -*-

"""
A Smart emulator.
Run Smart code one a emulator.
"""


from sys import argv
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from time import sleep
from pathlib import Path
import json
import os

from threading import Thread

from smart_compiller import compile_smarty, SmartError, CompileError

if "--debug" in argv:
    normal_speed = "Debug"
    argv.remove("--debug")
else:
    normal_speed = "1Mhz"


open_from_asm = False

if len(argv) != 2:
    file_name = ""
    code = ""
    def open_smart() -> None:
        """Use filedialoge for open a file."""
        global file_name, code, open_from_asm

        path = filedialog.askopenfilename(defaultextension="sma", filetypes=[("Smart source code", "*.sma"), ("Assembly", "*.asm")])


        if path:
            file_type = os.path.splitext(path)[1]

            if file_type == ".sma":
                file_name = path
            elif file_type == ".asm":
                asm_f = open(path, mode="r", encoding="UTF-8")

                code = asm_f.read()

                asm_f.close()

                open_from_asm = True


            else:
                messagebox.showerror("Error", f"Unknow file type {file_type}.")
            
            window_start.destroy()

    window_start = tk.Tk()
    window_start.title("Smart emulator")

    text_info = tk.Label(window_start, text="Open a Smart code source (*.sma) or open a Assembly (*.asm).\nCarful: with assembly, the emulator can have error...")
    text_info.pack()

    button_open = tk.Button(window_start, text="Open *.sma of *.asm", command=open_smart)
    button_open.pack()

    window_start.protocol("WM_DELETE_WINDOW", lambda:sys.exit(0))
    window_start.mainloop()
    

else:
    file_name = argv[1]

if file_name == "--asm-entry":
    code = input("Enter the assembly code : ")#.split(" ")

elif open_from_asm:pass

else:
    try:
        code = compile_smarty(file=file_name, argv=[], CODE_ADRESSE=1024, make_file=False)
    except SmartError as se:
        messagebox.showerror("Error", "Error during compilation of the Smart code.", detail=f"Detail: {se.syntaxerror}")
        sys.exit(1)

    except CompileError as ce:
        messagebox.showerror("Error", "Error during compilation of the Smart code.", detail=f"Detail: {ce.error}")
        sys.exit(1)

asm_code = code

ALLOW_CHAR = "!\"#$%'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_\n\r "
START_RAM = 0x2E7

window_emulator = tk.Tk()
window_emulator.title("Smart emulator")

monitor = scrolledtext.ScrolledText(window_emulator, height=24, width=39, bg="#000000", fg="#0099FF", insertwidth=10, insertbackground="#B1B1B1", insertofftime=0)
monitor.pack()
monitor.focus_force()
monitor.tag_configure("error", foreground="#FF0000")
monitor.tag_configure("sys_message", foreground="#00FF00")

def disable_edit(event:tk.Event) -> str:
    return "break"

monitor.bind("<Key>", disable_edit)

var_info_run = tk.StringVar(window_emulator)

text_info_run = tk.Label(window_emulator, textvariable=var_info_run)
text_info_run.pack()

frame_option = tk.Frame(window_emulator)
frame_option.pack()

def print_on_text(text:str, sys_message:bool=False, error:bool=False) -> None:
    """Insert on the scolledtext the text.
    If error = True, use tag for set the text one red."""
    text = text.replace("\r", "\n")

    if not sys_message:
        text = text.upper()
        if text not in ALLOW_CHAR:      # forbiden char
            return

    if error:
        monitor.insert(tk.END, text, "error")
    elif sys_message:
        monitor.insert(tk.END, text, "sys_message")
    else:
        monitor.insert(tk.END, text)
    monitor.see(tk.END)


def see_memory() -> None:
    """Open a window for see the memory (RAM, accumulator, carry_flag)."""
    def update_memory() -> None:
        """Update the listbox for memory"""
        # RAM
        pos_listbox = RAM_info.yview()[0]
        
        selection = RAM_info.curselection()
        selected_index = selection[0] if selection else None

        RAM_info.delete(0, tk.END)

        new_ram = (f"{adress}       {RAM[adress]}" for adress in RAM)

        RAM_info.insert(0, "Adress    Value")

        for adress in new_ram:
            RAM_info.insert(tk.END, adress)
        
        RAM_info.yview_moveto(pos_listbox)

        if selected_index is not None:
            RAM_info.selection_set(selected_index)
        
        # accumulator

        selection_acc = accumulator_info.curselection()
        selected_index_acc = selection_acc[0] if selection_acc else None

        accumulator_info.delete(0, tk.END)
        
        for ac in ("ACCUMULATOR    Value", f"A     " + accumulator["A"], f"X     " + accumulator["X"], f"Y     " + accumulator["Y"]):
            accumulator_info.insert(tk.END, ac)
        
        if selected_index_acc is not None:
            accumulator_info.selection_set(selected_index_acc)

        # flags
        pos_listbox_flags = flags_info.yview()[0]
        
        selection_flags = flags_info.curselection()
        selected_index_flags = selection_flags[0] if selection_flags else None

        flags_info.delete(0, tk.END)
        
        flags_info.insert(0, "Flag    Value")
        for flag_name, flag_value in flags.items():
            flags_info.insert(tk.END, f"{flag_name} = {flag_value}")
        
        flags_info.yview_moveto(pos_listbox_flags)

        if selected_index_flags is not None:
            flags_info.selection_set(selected_index_flags)

        window_memory.after(100, update_memory)

    window_memory = tk.Toplevel(window_emulator)
    window_memory.title("Memory")

    text_info = tk.Label(window_memory, text="Information about memory.\nYou can edit memory with double click on the value.\nCarful: editing memory can cause errors.")
    text_info.grid(column=0, row=0, columnspan=3)

    frame_RAM = tk.LabelFrame(window_memory, text="RAM")

    def edit_ram(event:tk.Event) -> None:
        """Open a window for edit the RAM value."""
        def validate() -> None:
            """Edit RAM with the new value."""
            new_value = entry_value.get()

            if len(new_value) != 2 or not all(c in "0123456789abcdefABCDEF" for c in new_value):
                messagebox.showerror("Error", "Invalid value. Please enter a hexadecimal value with 2 characters.")
                return
            
            RAM["0" + hex(adress)[2:].upper()] = new_value.upper()

            window.destroy()

        adress = RAM_info.curselection()[0] - 1 + START_RAM
        window = tk.Toplevel(window_memory)
        window.title("Edit RAM")


        text_info = tk.Label(window, text=f"Enter the new value for the RAM.\nCarful: editing memory can cause errors.\nAdress : {hex(adress)}")
        text_info.pack()

        entry_value = tk.Entry(window, width=5)
        entry_value.pack()

        button_validate = tk.Button(window, text="Validate", command=validate)
        button_validate.pack()

    def edit_accumulator(event:tk.Event) -> None:
        """Open a window for edit the accumulator value."""
        def validate() -> None:
            """Edit accumulator with the new value."""
            new_value = entry_value.get()

            if len(new_value) != 2 or not all(c in "0123456789abcdefABCDEF" for c in new_value):
                messagebox.showerror("Error", "Invalid value. Please enter a hexadecimal value with 2 characters.")
                return
            
            acc_index = accumulator_info.curselection()[0] - 1
            acc_keys = ["A", "X", "Y"]
            
            accumulator[acc_keys[acc_index]] = new_value.upper()

            window.destroy()

        acc_index = accumulator_info.curselection()[0] - 1
        acc_keys = ["A", "X", "Y"]
        acc_name = acc_keys[acc_index]
        
        window = tk.Toplevel(window_memory)
        window.title("Edit Accumulator")

        text_info = tk.Label(window, text=f"Enter the new value for the {acc_name} accumulator.\nCarful: editing memory can cause errors.")
        text_info.pack()

        entry_value = tk.Entry(window, width=5)
        entry_value.pack()

        button_validate = tk.Button(window, text="Validate", command=validate)
        button_validate.pack()

    scrollbar_RAM = tk.Scrollbar(frame_RAM)
    scrollbar_RAM.pack(side=tk.RIGHT, fill=tk.Y)

    RAM_info = tk.Listbox(frame_RAM, yscrollcommand=scrollbar_RAM.set)
    RAM_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_RAM.config(command=RAM_info.yview)
    RAM_info.bind("<Double-Button-1>", edit_ram)

    frame_RAM.grid(column=0, row=1)

    frame_accumulator = tk.LabelFrame(window_memory, text="Accumulator (register)")

    scrollbar_acc = tk.Scrollbar(frame_accumulator)
    scrollbar_acc.pack(side=tk.RIGHT, fill=tk.Y)

    accumulator_info = tk.Listbox(frame_accumulator, yscrollcommand=scrollbar_acc.set)
    accumulator_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_acc.config(command=accumulator_info.yview)
    accumulator_info.bind("<Double-Button-1>", edit_accumulator)

    frame_accumulator.grid(column=1, row=1)

    frame_flags = tk.LabelFrame(window_memory, text="Flags (6502)")

    def edit_flag(event:tk.Event) -> None:
        """Open a window for edit the flag value."""
        def validate() -> None:
            """Edit flag with the new value."""
            new_value = entry_value.get()

            if new_value not in ["0", "1"]:
                messagebox.showerror("Error", "Invalid value. Please enter 0 or 1.")
                return
            
            flag_index = flags_info.curselection()[0] - 1
            flag_keys = list(flags.keys())
            
            flags[flag_keys[flag_index]] = int(new_value)

            window.destroy()

        flag_index = flags_info.curselection()[0] - 1
        flag_keys = list(flags.keys())
        flag_name = flag_keys[flag_index]
        
        window = tk.Toplevel(window_memory)
        window.title("Edit Flag")

        text_info = tk.Label(window, text=f"Enter the new value for the {flag_name} flag.\nValue must be 0 or 1.")
        text_info.pack()

        entry_value = tk.Entry(window, width=5)
        entry_value.pack()

        button_validate = tk.Button(window, text="Validate", command=validate)
        button_validate.pack()

    scrollbar_flags = tk.Scrollbar(frame_flags)
    scrollbar_flags.pack(side=tk.RIGHT, fill=tk.Y)

    flags_info = tk.Listbox(frame_flags, yscrollcommand=scrollbar_flags.set)
    flags_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_flags.config(command=flags_info.yview)
    flags_info.bind("<Double-Button-1>", edit_flag)

    frame_flags.grid(column=0, row=2)


    update_memory()


button_RAM = tk.Button(frame_option, text="See memory", command=see_memory)
button_RAM.grid(column=0, row=0)

one_pause = False

def window_code() -> None:
    """Open a window for see the code and see the step."""
    def update_code() -> None:
        """Update the listbox for code"""
        pos_listbox = list_code.yview()[0]
        selection = list_code.curselection()
        selected_index = selection[0] if selection else None

        list_code.delete(0, tk.END)

        adress_conter = 0

        list_code.insert(0, "Adress    Code")

        for i in code[1:]:
            list_code.insert(tk.END, f"{hex(0x400 + adress_conter)}      {i}")
            adress_conter += 1
        
        list_code.yview_moveto(pos_listbox)

        if 0 <= run_step < list_code.size():
            list_code.itemconfig(run_step, {'bg':'#0099FF', 'fg':'#000000'})

        if selected_index is not None:
            list_code.selection_set(selected_index)

        window_code.after(100, update_code)

    window_code = tk.Toplevel(window_emulator)
    window_code.title("See code")

    text_info = tk.Label(window_code, text="See code\nDouble click on a line for edit the code.\nCarful: editing code can cause errors.")
    text_info.pack()

    frame_code = tk.Frame(window_code)
    frame_code.pack(expand=True, fill=tk.BOTH)

    scrollbar_code = tk.Scrollbar(frame_code)
    scrollbar_code.pack(side=tk.RIGHT, fill=tk.Y)

    list_code = tk.Listbox(frame_code, width=50, yscrollcommand=scrollbar_code.set)
    list_code.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    scrollbar_code.config(command=list_code.yview)

    def edit_code(event:tk.Event) -> None:
        """Open a window for edit the code."""
        def validate() -> None:
            """Edit code with the new value."""
            new_value = entry_value.get()

            if len(new_value) != 2 or not all(c in "0123456789abcdefABCDEF" for c in new_value):
                messagebox.showerror("Error", "Invalid value. Please enter a hexadecimal value with 2 characters.")
                return
            
            code_index = list_code.curselection()[0] - 1

            if code_index < 0:
                messagebox.showerror("Error", "You can't edit this line.")
                return
            
            code[code_index + 1] = new_value.upper()

            window.destroy()

        code_index = list_code.curselection()[0] - 1

        if code_index < 0:
            messagebox.showerror("Error", "You can't edit this line.")
            return
        
        window = tk.Toplevel(window_code)
        window.title("Edit code")

        text_info = tk.Label(window, text=f"Enter the new value for the code.\nCarful: editing code can cause errors.\nAdress : {hex(0x400 + code_index)}")
        text_info.pack()

        entry_value = tk.Entry(window, width=5)
        entry_value.pack()
        

        button_validate = tk.Button(window, text="Validate", command=validate)
        button_validate.pack()
    
    list_code.bind("<Double-Button-1>", edit_code)

    update_code()

    frame_setting = tk.Frame(window_code)
    frame_setting.pack()

    str_var_pause = tk.StringVar(frame_setting, value="Pause")

    def pause_code() -> None:
        """If the code is not in pause, set the pause, else, remove the pause."""
        global one_pause

        if one_pause:
            str_var_pause.set("Pause")
        else:
            str_var_pause.set("Play")

        one_pause = not one_pause

    button_pause = tk.Button(frame_setting, textvariable=str_var_pause, command=pause_code)
    button_pause.grid(column=0, row=0)

    frame_goto = tk.LabelFrame(frame_setting, text="Go to")
    frame_goto.grid(column=1, row=0)

    text_goto = tk.Label(frame_goto, text="Enter the adress to go (hexadecimal):")
    text_goto.pack()

    frame_entry = tk.Frame(frame_goto)
    frame_entry.pack()

    entry_goto = tk.Entry(frame_entry, width=10)
    entry_goto.grid(column=0, row=0)

    def goto_adress() -> None:
        """Go to the step of the code with the adress in entry_goto."""
        global run_step

        if end_run:
            messagebox.showerror("Error", "The code is already run. You can't go to an adress.")
            return

        try:
            adress = int(entry_goto.get(), base=16)
        except ValueError:
            messagebox.showerror("Error", "Invalid hexadecimal value. Please enter a valid hexadecimal number.")
            return
        
        if 0x400 <= adress < 0x400 + len(code) - 1:
            run_step = adress - 0x400 + 1
        else:
            messagebox.showerror("Error", f"Invalid adress. Please enter a hexadecimal value between {hex(0x400)} and {hex(0x400 + len(code) - 1)}.")
        
        

    button_goto = tk.Button(frame_entry, text="Go", command=goto_adress)
    button_goto.grid(column=1, row=0)

button_code = tk.Button(frame_option, text="See code", command=window_code)
button_code.grid(column=1, row=0)


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

    radio_speed_mos = tk.Radiobutton(window_setting, text="Run with a speed of 1Mhz\n(speed of MOS 6502)", variable=var_speed, value="1Mhz")
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
flags = {
    "C": 0,  # Carry
    "Z": 0,  # Zero
    "I": 0,  # Interrupt disable
    "D": 0,  # Decimal mode
    "B": 0,  # Break
    "V": 0,  # Overflow
    "N": 0   # Negative
}
run_step = 0
end_run = False

def pressed_key(event:tk.Event) -> str:
    """When a key are pressed, set ad D010 and D011 adress the key."""
    char = event.char.upper()
    
    if char not in ALLOW_CHAR:
        return "break"
    try:
        RAM["D010"] = hex(ord(char))[2:].upper()
        RAM["D011"] = "01"
    except:
        pass
    return "break"

window_emulator.bind("<KeyPress>", pressed_key)
monitor.bind("<KeyPress>", pressed_key)

def error_during_run() -> None:
    """Print an error message on the monitor."""
    print_on_text("\nError occurred during run...", True, True)

def set_flag_for_LD(byte_hex: str) -> None:
    v = int(byte_hex, 16) & 0xFF
    flags["Z"] = 1 if v == 0 else 0
    flags["N"] = 1 if (v & 0x80) else 0

def run_smart() -> None:
    """Run smart code."""
    global code, RAM, accumulator, flags, run_step, end_run

    code = code.split(" ")


    code = [x for x in code if x != ""]

    START = int(code[0][:-1], base=16)

    run_step = 1

    accumulator = {"A":"00", "X":"00", "Y":"00"}

    RAM = {"0" + hex(i)[2:].upper():"00" for i in range(0x02E7, 0x400 + 1)}
    RAM["D010"] = "00"
    RAM["D011"] = "00"

    run_fail = False

    return_ardess = 0

    while run_step < len(code):
        run = code[run_step]

        if one_pause:
            sleep(0.1)
            continue
        
        if " ".join(code[run_step:run_step + 7]) == "10 FB AD 10 D0 29 7F":     # special code:
            var_info_run.set("The programme is waiting for a key...")
            while RAM["D011"] == "00":
                sleep(0.1)        # wait for a key
            
            var_info_run.set("")
            
            RAM["D011"] = "00"
            accumulator["A"] = RAM["D010"]

            run_step += 7

        # normal instruction:

        elif run == "A9":     # A
            accumulator["A"] = code[run_step + 1]
            run_step += 2
            set_flag_for_LD(accumulator["A"])
        
        elif run == "A2":
            accumulator["X"] = code[run_step + 1]
            run_step += 2
            set_flag_for_LD(accumulator["X"])
        
        elif run == "A0":
            accumulator["Y"] = code[run_step + 1]
            run_step += 2
            set_flag_for_LD(accumulator["Y"])
        
        elif run == "8D":
            adress = code[run_step + 2] + code[run_step + 1]

            if 0x300 <= int(adress, base=16) >= 0x400:    # write one the programme
                try:
                    code[int(adress, base=16) - START + 1] = accumulator["A"]
                except:
                    messagebox.showerror("Error", "Write on unknow adress.", detail="Detail: {}".format(hex(0x400 + int(adress, base=16) - START + 1)).upper())
                    run_fail = True
                    break
            else:
                RAM[code[run_step + 2] + code[run_step + 1]] = accumulator["A"]

            run_step += 3

        elif run == "AD":
            accumulator["A"] = RAM[code[run_step + 2] + code[run_step + 1]]

            set_flag_for_LD(accumulator["A"])

            run_step += 3
        
        elif run == "20":
            run_step += 1

            code[run_step]

            if code[run_step] == "EF" and code[run_step + 1] == "FF":
                print_on_text(chr(int(accumulator["A"], base=16)))

                run_step += 2
            
            else:
                return_ardess = run_step + 2

                adress_call = int(code[run_step + 1] + code[run_step], base=16) - START + 1

                if adress_call + 0x400 >= 0x400 + len(code):
                    messagebox.showerror("Error", "Unknow adress for call.")
                    run_fail = True
                    break

                run_step = adress_call

        
        elif run == "00":
            break

        elif run == "60":
            run_step = return_ardess

        elif run == "4C":   # goto
            goto = code[run_step + 2] + code[run_step + 1]

            run_step = int(goto, base=16) - START + 1
        
        elif run == "18":
            flags["C"] = 0

            run_step += 1
        
        elif run == "69":
            add = code[run_step + 1]

            new_A = int(accumulator["A"], base=16) + int(add, base=16)

            if new_A >= 256:
                flags["C"] = 1
                flags["V"] = 1  # Set Overflow flag
                new_A -= 256
            else:
                flags["C"] = 0

            # Set Zero and Negative flags
            flags["Z"] = 1 if new_A == 0 else 0
            flags["N"] = 1 if new_A & 0x80 else 0

            accumulator["A"] = hex(new_A)[2:].upper().zfill(2)

            run_step += 2

        elif run == "C9" or run == "CD":       # compare A
            value = code[run_step + 1] if run == "C9" else RAM[code[run_step + 2] + code[run_step + 1]]

            result = int(accumulator["A"], base=16) - int(value, base=16)

            flags["C"] = 1 if result >= 0 else 0
            flags["Z"] = 1 if result == 0 else 0
            flags["N"] = 1 if result & 0x80 else 0

            run_step += 2 if run == "C9" else 3

        elif run == "D0":       # BNE
            offset = int(code[run_step + 1], base=16)

            if flags["Z"] == 0:
                run_step += 2 + offset
            else:
                run_step += 2

        elif run == "6D":
            RAM_adress = code[run_step + 2] + code[run_step + 1]
            

            add = RAM[RAM_adress]

            new_A = int(accumulator["A"], base=16) + int(add, base=16)

            if new_A >= 256:
                flags["C"] = 1
                flags["V"] = 1  # Set Overflow flag
                new_A -= 256
            else:
                flags["C"] = 0


            flags["Z"] = 1 if new_A == 0 else 0
            flags["N"] = 1 if new_A & 0x80 else 0

            accumulator["A"] = hex(new_A)[2:].upper().zfill(2)

            run_step += 3
        
        else:
            messagebox.showerror("Error", f"Unknow assembly : {run}, at {run_step} step.")
            run_fail = True
            break

        if normal_speed == "1Mhz":
            sleep(0.0025)
        elif normal_speed == "Debug":
            sleep(1.5)
    
    end_run = True

    print_on_text("\n\nEnd of run", True)

    if run_fail:
        error_during_run()
   
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
        data = {"RAM": RAM, "accumulator": accumulator, "carry_flag": flags["C"]}

        Path(file_path).write_text(json.dumps(data, indent=4), encoding="utf-8")

menu_save.add_command(label="Save memory (as *.json)", command=export_memory)

def save_asm() -> None:
    """Save the assembly code in a *.asm file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".asm", filetypes=[("Assembly files", "*.asm")])

    if file_path:
        Path(file_path).write_text(asm_code, encoding="utf-8")

menu_save.add_command(label="Save assembly (as *.asm)", command=save_asm)

def start_run() -> None:
    """Call run_smart."""
    try:
        run_smart()
    except IndexError:
        messagebox.showerror("Error", "Error with adress.")
        error_during_run()

    except Exception as e:
        messagebox.showerror("Error", "Error during run.", detail=f"Detail: {str(e)}")
        error_during_run()

thread_run = Thread(target=start_run, daemon=True)
thread_run.start()


window_emulator.mainloop()
