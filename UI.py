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
        self.left_label_width = 15
        self.editbox_width = 50
        self.option_add('*TCombobox*Listbox.font', self.font)
        self.__api_methods = ("Организации (/api/1/organizations)", "Терминалы (/api/1/terminal_groups)", "Типы оплат (/api/1/payment_types)",
                              "Типы заказов (/api/1/deliveries/order_types)", "Доставки по дате (/deliveries/by_delivery_date_and_status)",
                              "Меню/Выгрузка меню (/1/nomenclature)", "Внешнее меню (/2/menu)", "Выгрузка из внешнего меню (/2/menu/by_id)")

        #   Initialize graphic objects of main window
        #   Labels (heads of interactive objects)
        self.org_label = tk.Label(self, text="Название", width=self.left_label_width, font=self.font, anchor="w")
        self.key_label = tk.Label(self, text="API ключ", width=self.left_label_width, font=self.font, anchor="w")
        self.method_label = tk.Label(self, text="API Запрос", width=self.left_label_width, font=self.font, anchor="w")
        self.json_request_label = tk.Label(self, text="JSON", width=self.left_label_width, font=self.font, anchor="w")
        self.json_tips_label = tk.Label(self, text="Подсказки по JSON", font=self.font, anchor="w")
        self.json_status_label = tk.Label(self, text="Response Status", font=("Arial", 14), fg="green", anchor="e")
        self.json_response_label = tk.Label(self, text="JSON Ответ", font=self.font)
        self.url_label = tk.Label(self, text="URL: https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_status", font=self.font, anchor="w")

        #Drop lists (Comboboxes)
        self.org_box = ttk.Combobox(self, width=self.editbox_width, font=self.font)
        self.key_box = ttk.Combobox(self, width=self.editbox_width, font=self.font)
        self.method_box = ttk.Combobox(self, width=self.editbox_width, font=self.font, values=self.__api_methods)

        #Buttons
        self.db_append_btn = tk.Button(self, text="Добавить в справочник ключ", font=self.font)
        self.send_request_btn = tk.Button(self, text="Выполнить запрос")

        #Text boxes
        self.json_request_box = tk.Text(self, width=self.editbox_width+self.left_label_width, height = 50, font=self.font,
                                            wrap="none")
        self.json_tips_box = tk.Text(self, width=30, height = 30, font=self.font, wrap="none")
        self.json_response_box = tk.Text(self, width=30, height = 30, font=self.font, wrap="none")

        loggerUI.info("Main window objects initialized")

        self.widgets_place()
        loggerUI.info("Initialized objects placed on main window successfully")


        #Function that places objects initialized earlier
    def widgets_place(self):
        self.org_label.place(x=2, y=3, width=80)
        self.org_box.place(x=80, y=3, relwidth=0.4)
        self.key_label.place(x=2, y=26, width=80)
        self.key_box.place(x=80, y=26, relwidth=0.4)
        self.method_label.place(x=2, y=49, width=80)
        self.method_box.place(x=80, y=49, relwidth=0.4)
        self.json_status_label.place(relx=0.7, y=3,  relwidth=0.3, height=55)
        self.db_append_btn.place(x=2, y=71, width=185)
        self.url_label.place(x=2, y=97, width=450)
        self.json_request_label.place(x=2, y=115, width=38)
        #self.box



