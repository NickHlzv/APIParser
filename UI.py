import tkinter as tk
import tkinter.ttk as ttk
import logging
import tkinter.messagebox as messagebox

logging.basicConfig(level=logging.INFO, filename="app.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


class UIMain(tk.Tk):
    def __init__(self, master=None, form_name="Test", form_size="1024x768"):
        super().__init__(master)
        self.key_label, self.key_combobox, self.method_label, self.method_combobox = None, None, None, None
        self.create_keybox(["arfasad-asdsa", "sgfdgfd-asda"])
        self.create_methodbox(["Организации", "Терминалы"])
        self.title(form_name)
        self.resizable(False, False)
        self.geometry(form_size)

    def create_keybox(self, menu:list, name="API key", width=50, font=("Arial", 10)):
        self.key_label = ttk.Label(self, text=name, width=width, font=font)
        self.key_label.pack()
        self.key_combobox = ttk.Combobox(self, values=menu, width=width, font=font)
        self.key_combobox.pack()

    def create_methodbox(self, menu:list, name="API Запрос", width=50, font=("Arial", 10)):
        self.method_label = ttk.Label(self, text=name, width=width, font=font)
        self.method_label.pack()
        self.method_combobox = ttk.Combobox(self, values=menu, width=width, font=font, state="readonly")
        self.method_combobox.pack()

        self.btnHello = ttk.Button(self, text="Пpивeтcтвoвaть\nпoльзoвaтeля")
        self.btnHello.bind("<ButtonRelease>", self.say_hello)
        self.btnHello.pack()
        self.btnShow = ttk.Button(self)
        self.btnShow["text"] = "Выход"
        self.btnShow["command"] = self.destroy
        self.btnShow.pack(side="bottom")

    def say_hello(self, evt):
        tk.messagebox.showinfo("Test", "Привет, пользователь!")


