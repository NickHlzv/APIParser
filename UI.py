import tkinter as tk
import tkinter.ttk as ttk
import logging
import tkinter.messagebox as messagebox

#Подключение логгирования модуля UI.py
logging.basicConfig(level=logging.INFO, filename="app.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


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
        self.org_label = tk.Label(self, text="Название", width=self.left_label_width, font=self.font)
        self.key_label = tk.Label(self, text="API ключ", width=self.left_label_width, font=self.font)
        self.method_label = tk.Label(self, text="API Запрос", width=self.left_label_width, font=self.font)
        self.json_request_label = tk.Label(self, text="JSON", width=self.left_label_width, font=self.font)
        self.json_tips_label = tk.Label(self, text="Подсказки по JSON", font=self.font)
        self.json_status_label = tk.Label(self, text="<JSON Status>", font=("Arial", 14), fg="green")
        self.json_response_label = tk.Label(self, text="JSON Ответ", font=self.font)

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

        logging.info("Main window objects initialized")

        self.widgets_pack()
        logging.info("Initialized objects placed on main window successfully")


        #Функция отвечающая за ращмещение ранее объявленных объектов окна
    def widgets_pack(self):
        pady = 1
        self.org_label.pack(anchor="nw", pady=pady)
        self.org_box.pack(anchor="n", pady=pady)
        self.key_label.pack(anchor="nw", pady=pady)
        self.key_box.pack(anchor="n", pady=pady)
        self.method_label.pack(anchor="nw", pady=pady)
        self.method_box.pack(anchor="n", pady=pady)


