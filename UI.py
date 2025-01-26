import tkinter as tk
import tkinter.ttk as ttk
import logging

#   Set logging module UI.py

loggerUI = logging.getLogger(__name__)
loggerUI.setLevel(logging.INFO)

handlerUI = logging.FileHandler(f"{__name__}.log")
handlerUI.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))
loggerUI.addHandler(handlerUI)


class UIMain(tk.Tk):
    def __init__(self, master=None, form_name="Test", form_size="1024x768"):
        super().__init__(master)

        #  Initialize attributes of main window
        self.title(form_name)
        #self.resizable(False, False)
        self.geometry(form_size)
        self.font = ("Arial", 10)
        self.option_add('*TCombobox*Listbox.font', self.font)
        self.__apiMethods = ("Организации (/api/1/organizations)", "Терминалы (/api/1/terminal_groups)", "Типы оплат (/api/1/payment_types)",
                              "Типы заказов (/api/1/deliveries/order_types)", "Доставки по дате (/deliveries/by_delivery_date_and_status)",
                              "Меню/Выгрузка меню (/1/nomenclature)", "Внешнее меню (/2/menu)", "Выгрузка из внешнего меню (/2/menu/by_id)")

        #   Initialize graphic objects of main window
        #   Labels (heads of interactive objects)
        self.orgLabel = tk.Label(self, text="Название", font=self.font, anchor="w")
        self.keyLabel = tk.Label(self, text="API ключ", font=self.font, anchor="w")
        self.methodLabel = tk.Label(self, text="API Запрос", font=self.font, anchor="w")
        self.jsonRequestLabel = tk.Label(self, text="JSON", font=self.font, anchor="w")
        self.jsonTipsLabel = tk.Label(self, text="Подсказки по JSON", font=self.font, anchor="w")
        self.jsonStatusLabel = tk.Label(self, text="Response Status", font=("Arial", 14), fg="green", anchor="e")
        self.jsonResponseLabel = tk.Label(self, text="JSON Ответ", font=self.font)
        self.urlLabel = tk.Label(self, text="URL: https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_status",
                                  font=self.font, anchor="w")

        #Drop lists (Comboboxes)
        self.orgBox = ttk.Combobox(self, font=self.font)
        self.keyBox = ttk.Combobox(self, font=self.font)
        self.methodBox = ttk.Combobox(self, font=self.font, values=self.__apiMethods)

        #Buttons
        self.dbAppendBtn = tk.Button(self, text="Добавить в справочник ключ", font=self.font)
        self.sendRequestBtn = tk.Button(self, text="Выполнить")

        #Text boxes
        self.jsonRequestBox = tk.Text(self, height = 50, font=self.font,
                                            wrap="none")
        self.jsonTipsBox = tk.Text(self, width=30, height = 30, font=self.font, wrap="none")
        self.jsonResponseBox = tk.Text(self, width=30, height = 30, font=self.font, wrap="none")

        loggerUI.info("Main window objects initialized")

        self.widgets_place()
        loggerUI.info("Initialized objects placed on main window successfully")


        #Function that places objects initialized earlier
    def widgets_place(self):
        self.orgLabel.place(x=2, y=3, width=80)
        self.orgBox.place(x=80, y=3, relwidth=0.4)
        self.keyLabel.place(x=2, y=26, width=80)
        self.keyBox.place(x=80, y=26, relwidth=0.4)
        self.methodLabel.place(x=2, y=49, width=80)
        self.methodBox.place(x=80, y=49, relwidth=0.4)
        self.jsonStatusLabel.place(relx=0.7, y=3,  relwidth=0.3, height=55)
        self.dbAppendBtn.place(x=2, y=71, width=185)
        self.urlLabel.place(x=2, y=97, width=450)
        self.jsonRequestLabel.place(x=2, y=115, width=38)
        self.jsonRequestBox.place(x=2, y=135, relwidth=0.37, relheight=0.8)
        self.jsonTipsBox.place(relx=0.37, y=135, relwidth=0.25, relheight=0.8)




