import tkinter as tk
import tkinter.ttk as ttk

class NamedCombobox(ttk.Combobox, ttk.Label):
    def __init__(self, menu:list, master=None, name="Имя поля", width=50, font=("Arial", 10)):
        super().__init__(master)
        self.label_combobox = ttk.Label(self, text=name, width=width, font=font)
        self.combobox = ttk.Combobox(self, values=menu, width=width, font=font)

    def pack(self, anchor="nw", padx=0, pady=0):

        self.label_combobox.pack(anchor=anchor, padx=padx, pady=pady)
        self.combobox.pack(anchor=anchor)


class NamedTextbox(tk.Text, tk.Label):
    def __init__(self, master=None, name="Имя поля", width=50, height=100, font=("Arial", 10)):
        super().__init__(master)
        self.label_text = tk.Label(self, text=name, width=width, font=font)
        self.textbox = tk.Text(self, width=width, height=height, font=font)


    def pack(self, anchor="nw", padx=0, pady=0):
        self.label_text.pack(anchor=anchor, padx=padx, pady=pady)
        self.textbox.pack(anchor=anchor)


class UIMain(ttk.Frame):
    def __init__(self, master=None, form_name="Application", form_size="1024x768"):
        super().__init__(master)
        self.pack()
        self.master.title(form_name)
        self.master.resizable(False, False)
        self.master.geometry(form_size)
        ui_font = ("Arial", 14)
        self.company_name_box = NamedCombobox(["Жар-пицца", "Италиан-пицца"], name="Ввод Организации")
        self.company_name_box.pack(anchor="nw")
        self.company_name_box.pack(anchor="nw")
        self.apikey_box = NamedCombobox(["arfasad-asdsa", "sgfdgfd-asda"], name="Ввод API ключа")
        self.apikey_box.pack(pady=5, anchor="nw")
        self.apikey_box.pack(pady=5, anchor="nw")
        self.company_edit_name = NamedCombobox(["Жар-пицца", "Италиан-пицца"], name="Изменение Организации")
        self.company_edit_name.pack(anchor="n")
        self.label = ttk.Label(text="Имя поля", width=50, font=("Arial", 10))
        self.label.pack(anchor="nw")
        self.apikey_edit_box = NamedCombobox(["arfasad-asdsa", "sgfdgfd-asda"], name="Изменение API ключа")
        self.apikey_edit_box.pack(pady=5, anchor="n")








