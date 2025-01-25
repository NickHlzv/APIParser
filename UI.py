import tkinter as tk
import tkinter.ttk as ttk
import logging

#Подключение логгирования модуля UI.py

loggerUI = logging.getLogger(__name__)
loggerUI.setLevel(logging.INFO)

handlerUI = logging.FileHandler(f"{__name__}.log")
handlerUI.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))
loggerUI.addHandler(handlerUI)


class UIMain(tk.Tk):
    def __init__(self, master=None, form_name="Test", form_size="1024x768"):
        super().__init__(master)
        #Инициализация параметров главного окна
        self.title(form_name)
        self.resizable(False, False)
        self.geometry(form_size)
        self.font = ("Arial", 10)
        self.left_label_width = 15
        self.editbox_width = 60
        self.__api_methods = ("Организации (/api/1/organizations)", "Терминалы (/api/1/terminal_groups)", "Типы оплат (/api/1/payment_types)",
                              "Типы заказов (/api/1/deliveries/order_types)", "Доставки по дате (/deliveries/by_delivery_date_and_status)",
                              "Меню/Выгрузка меню (/1/nomenclature)", "Внешнее меню (/2/menu)", "Выгрузка из внешнего меню (/2/menu/by_id)")

        #Инициализация объектов главного окна
        #Метки (названия и статус полей)
        self.org_label = ttk.Label(self, text="Название", width=self.left_label_width, font=self.font, anchor="w")
        self.key_label = tk.Label(self, text="API ключ", width=self.left_label_width, font=self.font, anchor="w")
        self.method_label = tk.Label(self, text="API Запрос", width=self.left_label_width, font=self.font, anchor="w")
        self.json_request_label = tk.Label(self, text="JSON", width=self.left_label_width, font=self.font, anchor="w")
        self.json_tips_label = tk.Label(self, text="Подсказки по JSON", font=self.font, anchor="w")
        self.json_status_label = tk.Label(self, text="<JSON Status>", font=("Arial", 14), fg="green", anchor="w")
        self.json_response_label = tk.Label(self, text="JSON Ответ", font=self.font, anchor="w")

        #Выпадающие списки
        self.org_box = ttk.Combobox(self, width=self.editbox_width, font=self.font)
        self.key_box = ttk.Combobox(self, width=self.editbox_width, font=self.font)
        self.method_box = ttk.Combobox(self, width=self.editbox_width, font=self.font, values=self.__api_methods)

        #Кнопки
        self.db_append_btn = ttk.Button(self, text="Добавить в справочник ключ")
        self.send_request_btn = ttk.Button(self, text="Выполнить запрос")

        #Текстовые поля
        self.json_request_box = tk.Text(self, width=self.editbox_width+self.left_label_width, height = 50, font=self.font,
                                            wrap="none")
        self.json_tips_box = tk.Text(self, width=30, height = 30, font=self.font, wrap="none")
        self.json_response_box = tk.Text(self, width=30, height = 30, font=self.font, wrap="none")

        loggerUI.info("Main window objects initialized")

        self.widgets_pack()
        loggerUI.info("Initialized objects placed on main window successfully")


        #Функция отвечающая за ращмещение ранее объявленных объектов окна
    def widgets_pack(self):
        self.org_label.place(x=2, y=3, )
        self.org_box.place(x=2+self.editbox_width, y=3)
        self.key_label.place(x=2, y=26)
        self.key_box.place(x=2+self.editbox_width, y=26)
        self.method_label.place(x=2, y=49)
        self.method_box.place(x=2+self.editbox_width, y=49)


