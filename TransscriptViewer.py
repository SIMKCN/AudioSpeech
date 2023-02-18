import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
from pygame import mixer
import csv
def datei():
    global text1
    
    filename = askopenfilename()
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        content = list(csv_reader)
        for row in content:
            listbox.insert(tk.END, row)

chunkloader = tk.Tk()
chunkloader.geometry("1000x600")
scrollbar = tk.Scrollbar(chunkloader)
scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

load = tk.Button(chunkloader, text="Open", command=datei)
listbox = tk.Listbox(chunkloader, height = 1550, width = 300, bg = "grey", activestyle = "dotbox", fg = "black", selectmode="SINGLE")

load.pack(ipadx=10, ipady=10)
listbox.config(yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, expand=True, fill=tk.Y)
chunkloader.mainloop()
