import tkinter

from UI import *


#root = tk.Tk()
#app_menu = tkinter.ttk.Combobox(root)
#tkinter.ttk.
#app_menu.pack()
#root.mainloop()
#tk.Frame

#frm = ttk.Frame(root, padding=10, borderwidth=1, relief=SOLID)
#frm1 = ttk.Frame(root, padding = 10, borderwidth=1, relief=SOLID)
#frm.grid(column=0, row=0)
#frm1.grid(column=1, row=0)
#ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#ttk.Label(frm1, text="Hello World!").grid(column=0, row=0)
#ttk.Button(frm1, text="Quit", command=root.destroy).grid(column=1, row=0)
#root.mainloop()

root = tkinter.Tk()
root.geometry("1024x768")
app = UIMain(root)
#table = ttk.Treeview(app, show="tree")

root.mainloop()





