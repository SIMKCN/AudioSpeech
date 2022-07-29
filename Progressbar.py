import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x120")
root.title('Progressbar Demo')
root.grid()
pb = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=280)
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
start_button = ttk.Button(root, text='Start', command=pb.start)
start_button.grid(column=0, row=1, padx=10, pady=10, sticky=tk.E)
stop_button = ttk.Button(root, text='Stop', command=pb.stop)
stop_button.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)
root.mainloop()
