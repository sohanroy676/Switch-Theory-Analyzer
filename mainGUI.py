import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from core import Function

Func = Function()

def fromTable():
    global minmax_label
    Func.setFunction(input_var.get())
    truthTable, minTerms, maxTerms = Func.table()
    
    table = ttk.Treeview(master = mid_frame, columns = ["Num"] + [i for i in Func.varNames] + ["Result"], show = "headings")
    tables.append(table)
    for i in Func.varNames:
        table.heading(i, text = i)
        table.column(i, anchor = tk.CENTER)
    table.heading("Result", text = "Result")
    table.column("Result", anchor = tk.CENTER)
    table.heading("Num", text = "Num")
    table.column("Num", anchor = tk.CENTER)
    
    for idx, val in enumerate(truthTable):
        table.insert(parent = '', index = idx, values = val)
    
    table.pack(padx = 10, pady = 10, expand = True, fill = tk.BOTH)
    minmax_label = ctk.CTkLabel(master = mid_frame, text = f"Minterms: {minTerms}\nMaxterms: {maxTerms}", font = FONT)
    minmax_label.pack(padx = 10, pady = 10)

def fromMinterms():
    minTerms: list[int] = list(map(int, input_var.get().split()))
    dontCares: list[int] = list(map(int, dontcare_var.get().split()))
    
    func: str = Func.fromMinTerms(minTerms, dontCares)
    funcLen: int = len(func)

    cols = (("Group", "Matched Pair", ''.join(Func.varNames)), ("MinTerms", "Term", "Grouping"))
    for i, val in enumerate(func):
        colIndex = 1 if i == funcLen - 1 else 0
        table = ttk.Treeview(master = mid_frame, columns = cols[colIndex], show = "headings")
        tables.append(table)
        for c in cols[colIndex]:
            table.heading(c, text = c)
            table.column(c, anchor = tk.CENTER)
        idx = 0
        for m, t, g in (val, zip(*val))[colIndex]:
            table.insert(parent = '', index = idx, values = (m, t, g))
            idx += 1
        
        table.pack(padx = 10, pady = 10, expand = True, fill = tk.X)

def save_to_file():
    with open("D:\\Programming\\Python\\LST\\file.txt", "a") as f:
        f.write(f"{Func.minTerms}")
        f.close()

def run():
    global tables, minmax_label
    Func.reset()
    Func.setVariables(using_var.get().split())
    mode = mode_var.get()
    if tables:
        for table in tables:
            table.destroy()
        tables = []
    if minmax_label is not None:
        minmax_label.destroy()
        minmax_label = None
    try:
        if mode == "Function":
            fromTable()
        else:
            fromMinterms()
    except ValueError:
        print("Error Occurred")

TYPEFACE: str = "Calisto MT"
FONTSIZE: int = 20
FONT = (TYPEFACE, FONTSIZE)

# window
window = ctk.CTk()
window.title("Logic and Switching Theory")
width: int = 1200
height: int = 720
window.geometry(f"{width}x{height}+150+50")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=FONTSIZE*2,
                fieldbackground="#343638",
                bordercolor="#343638",
                border = "sunken",
                borderwidth=5,
                font = FONT)

style.map('Treeview', background=[('selected', '#22559b')])

style.configure("Treeview.Heading",
                background="#565b5e",
                foreground="white",
                relief="sunken",
                font = FONT)

style.map("Treeview.Heading",
            background=[('active', '#3484F0')])

style.map("Treeview.Col",)

title_label = ctk.CTkLabel(window, text="Switch Theory Analyzer", font=(TYPEFACE,30))
title_label.pack(pady = 5)

mid_frame = ctk.CTkScrollableFrame(window, fg_color="#333")
mid_frame.pack(padx=10, pady=10, expand = True, fill=tk.BOTH)

tables = []
minmax_label = None

input_frame = ctk.CTkFrame(window, fg_color="#555")
input_frame.pack(padx=10, pady=10, fill=tk.X)

subinput1_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
subinput1_frame.pack(fill=tk.X, expand = True)

input_var = tk.StringVar(value = "Func/Terms")
input_entry = ctk.CTkEntry(subinput1_frame, font=FONT, textvariable = input_var)
input_entry.pack(padx = (0, 10), pady = 10, side = tk.LEFT, expand = True, fill = tk.X)

dontcare_var = tk.StringVar(value = "Dont Cares")
dontcare_entry = ctk.CTkEntry(subinput1_frame, font=FONT, textvariable = dontcare_var)
dontcare_entry.pack(padx = (0, 10), pady = 10, side = tk.LEFT, expand = True, fill = tk.X)

enter_button = ctk.CTkButton(subinput1_frame, text = "ENTER", border_width = 5, corner_radius=10, border_color = "#000", font = FONT, command = run)
enter_button.pack(padx = 10, pady = 10, side = tk.LEFT)

subinput2_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
subinput2_frame.pack(pady = 10, fill=tk.X, expand = True, side = tk.TOP)

mode_label = ctk.CTkLabel(subinput2_frame, text="MODE: ", font = FONT)
mode_label.pack(padx = (20, 10), side = tk.LEFT)

mode_var = tk.StringVar(value = "Function")
mode_segbutton = ctk.CTkSegmentedButton(subinput2_frame, values=["Function", "MinTerms"], variable = mode_var, font = FONT)
mode_segbutton.pack(padx = (0, 30), side = tk.LEFT)

using_label = ctk.CTkLabel(subinput2_frame, text="USING: ", font = FONT)
using_label.pack(padx = (30, 0), side = tk.LEFT)

using_var = tk.StringVar(value = "x y z")
using_entry = ctk.CTkEntry(subinput2_frame, font=FONT, textvariable = using_var)
using_entry.pack(padx = (0, 10), pady = 10, side = tk.LEFT)

newEPI_var = tk.BooleanVar(value = False)
newEPI = ctk.CTkCheckBox(subinput2_frame, font = FONT, text = "Use new EPI (WIP)", variable = newEPI_var, onvalue = True, offvalue = False, command = exec("Func.newEPI = newEPI_var.get()"))
newEPI.pack(padx = 20, side = tk.LEFT)

save_button = ctk.CTkButton(subinput2_frame, font = FONT, text = "Save", command = save_to_file, border_width = 5, corner_radius=10, border_color = "#000")
save_button.pack(padx = 20, side = tk.RIGHT)

# mainloop
window.mainloop()