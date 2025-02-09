from tkinter import font as tkfont
import tkinter as tk
import tkinter.ttk as ttk
import logging
from API import APITrnRequest
from DB import *
import pymongo

#  Set logging module UI.py

loggerUI = logging.getLogger(__name__)
loggerUI.setLevel(logging.INFO)
handlerUI = logging.FileHandler(f"{__name__}.log", encoding='utf-8')
handlerUI.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))
loggerUI.addHandler(handlerUI)

#  Set general UI font
ui_font = ("Arial", 10)


#  Redefine new class of Textbox with simple RightClick menu from standard Textbox
class TextContext(tk.Text):
    """
    Extended text widget that includes a context menu
    with Copy, Cut and Paste commands.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Копировать", command=self.popup_copy)
        self.menu.add_command(label="Вырезать", command=self.popup_cut)
        self.menu.add_command(label="Вставить", command=self.popup_paste)
        self.bind("<Button-3>", self.display_popup)

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def popup_copy(self):
        self.event_generate("<<Copy>>")

    def popup_cut(self):
        self.event_generate("<<Cut>>")

    def popup_paste(self):
        self.event_generate("<<Paste>>")


#  Redefine new class of Entry with simple RightClick menu from standard Textbox
class EntryContext(tk.Entry):
    """
    Extended entry widget that includes a context menu
    with Copy, Cut and Paste commands.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Копировать", command=self.popup_copy)
        self.menu.add_command(label="Вырезать", command=self.popup_cut)
        self.menu.add_command(label="Вставить", command=self.popup_paste)
        self.bind("<Button-3>", self.display_popup)

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def popup_copy(self):
        self.event_generate("<<Copy>>")

    def popup_cut(self):
        self.event_generate("<<Cut>>")

    def popup_paste(self):
        self.event_generate("<<Paste>>")


#   Redefine new class of Combobox with simple RightClick menu from standard Textbox
class ComboboxContext(ttk.Combobox):
    """
    Extended combobox widget that includes a context menu
    with Copy, Cut and Paste commands.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Копировать", command=self.popup_copy)
        self.menu.add_command(label="Вырезать", command=self.popup_cut)
        self.menu.add_command(label="Вставить", command=self.popup_paste)
        self.bind("<Button-3>", self.display_popup)

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def popup_copy(self):
        self.event_generate("<<Copy>>")

    def popup_cut(self):
        self.event_generate("<<Cut>>")

    def popup_paste(self):
        self.event_generate("<<Paste>>")


#   Define class for dialog window that adds data to DB
class DialogWindow(tk.Toplevel):
    def __init__(self, form_name="Добавить API ключ", form_size="400x100", font=ui_font):
        # Init params and objects for dialog window
        super().__init__()
        self.font = font
        self.iconbitmap("logo.ico")
        self.title(form_name)
        self.resizable(False, False)
        self.geometry(form_size)

        self.orgLabel = tk.Label(self, text="Название", font=self.font, anchor="w")
        self.keyLabel = tk.Label(self, text="API ключ", font=self.font, anchor="w")
        self.orgEntry = EntryContext(self, font=self.font)
        self.keyEntry = EntryContext(self, font=self.font)
        self.dbAppendBtn = tk.Button(self, text="Добавить", font=self.font, command=self.insert_keys)
        self.statusLabel = tk.Label(self, text="Статус", font=self.font, anchor="w", fg="green")

        loggerUI.info("Dialog window objects initialized")

        self.widgets_place()

    # Function that places objects initialized earlier
    def widgets_place(self):
        self.orgLabel.place(x=2, y=3, width=80)
        self.orgEntry.place(x=80, y=3, width=300)
        self.keyLabel.place(x=2, y=26, width=80)
        self.keyEntry.place(x=80, y=26, width=300)
        self.dbAppendBtn.place(x=2, y=70, width=140)
        self.statusLabel.place(x=2, y=48, width = 380)
        loggerUI.info("Initialized objects placed on dialog window successfully")

    # define closing dialog window
    def dismiss(self):
        self.grab_release()
        self.destroy()
        loggerUI.info("Dialog window closed")

    # define function for button inserting keys into DB
    def insert_keys(self):
        apikey = self.keyEntry.get()
        api_name = self.orgEntry.get()

        if not apikey or len(apikey) < 8:
            if not api_name or len(api_name) < 5:
                loggerUI.info(f"Invalid API key and name")
                self.statusLabel["fg"] = "red"
                self.statusLabel["text"] = "Введите валидный Api key и название больше 4 символов"
            else:
                loggerUI.info(f"Invalid API key, name is valid")
                self.statusLabel["fg"] = "red"
                self.statusLabel["text"] = "Введите валидный Api key"
        else:
            if not api_name or len(api_name) < 5:
                loggerUI.info(f"API key is valid but name isn't valid")
                self.statusLabel["fg"] = "red"
                self.statusLabel["text"] = "Введите название больше 5 символов"
            else:
                status = False
                loggerUI.info(f"API key and name validated, try to save into DB")
                try:
                    db_client = MongoDB()
                    status, self.statusLabel["text"] = db_client.insert_key(api_name, apikey)
                    if status:
                        self.statusLabel["fg"] = "green"
                        loggerUI.info(f"Successfully inserted/updated API key into DB")
                    else:
                        self.statusLabel["fg"] = "red"
                        loggerUI.error(f"Failed to insert/update API key into DB, (does API key correct and exists?)")
                    db_client.close()
                except pymongo.errors.AutoReconnect:
                    self.statusLabel["fg"] = "red"
                    self.statusLabel["Text"] = "Не могу подключиться к базе, переподключаюсь"
                    loggerUI.exception("Failed connecting to DB. App can't work correctly")


#   Define main window class

class UIMain(tk.Tk):
    @staticmethod
    def create_window():
        loggerUI.info("Click on button 'Добавить в справочник ключ' on main window")
        #  Create an object of dialog window from class
        dialog_window = DialogWindow()
        #  Intercept clicking on cross button in a right corner
        dialog_window.protocol("WM_DELETE_WINDOW", lambda: dialog_window.dismiss())
        #  Intercept of input on application forms to dialog window
        dialog_window.grab_set()

    def __init__(self, form_name="API Parser", form_size="1024x768", font=ui_font):
        super().__init__()

        #  Initialize attributes of main window
        self.title(form_name)
        self.iconbitmap("logo.ico")
        self.geometry(form_size)
        self.font = font
        self.option_add('*TCombobox*Listbox.font', self.font)

        # initialize static menu data
        self.__apiMethods = (
            "Организации (/api/1/organizations)", "Терминалы (/api/1/terminal_groups)",
            "Типы оплат (/api/1/payment_types)",
            "Типы заказов (/api/1/deliveries/order_types)",
            "Доставки по дате (/deliveries/by_delivery_date_and_status)",
            "Меню/Выгрузка меню (/1/nomenclature)", "Внешнее меню (/2/menu)",
            "Выгрузка из внешнего меню (/2/menu/by_id)")

        self.__url_dict = {self.__apiMethods[0]: "https://api-ru.iiko.services/api/1/organizations",
                           self.__apiMethods[1]: "https://api-ru.iiko.services/api/1/terminal_groups",
                           self.__apiMethods[2]: "https://api-ru.iiko.services/api/1/payment_types",
                           self.__apiMethods[3]: "https://api-ru.iiko.services/api/1/deliveries/order_types",
                           self.__apiMethods[4]:
                               "https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_status",
                           self.__apiMethods[5]: "https://api-ru.iiko.services/api/1/nomenclature",
                           self.__apiMethods[6]: "https://api-ru.iiko.services/api/2/menu",
                           self.__apiMethods[7]: "https://api-ru.iiko.services/api/2/menu/by_id",
                           }

        #   Initialize graphic objects of main window
        #   Labels (heads of interactive objects)
        self.orgLabel = tk.Label(self, text="Название", font=self.font, anchor="w")
        self.keyLabel = tk.Label(self, text="API ключ", font=self.font, anchor="w")
        self.methodLabel = tk.Label(self, text="API Запрос", font=self.font, anchor="w")
        self.jsonRequestLabel = tk.Label(self, text="JSON", font=self.font, anchor="w")
        self.jsonTipsLabel = tk.Label(self, text="Подсказки по JSON", font=self.font, anchor="w")
        self.jsonStatusLabel = tk.Label(self, text="Response Status", font=("Arial", 14), fg="green", anchor="e")
        self.jsonResponseLabel = tk.Label(self, text="JSON Ответ", font=self.font, anchor="e")
        self.urlLabel = tk.Label(self, text="URL: https://api-ru.iiko.services/api/1/organizations",
                                 font=self.font, anchor="w")

        self.searchEntry = EntryContext(self, font=self.font)
        self.searchEntry.bind("<Return>", self.search_res_ev)

        #Drop lists (Comboboxes)
        self.orgBox = ComboboxContext(self, font=self.font)
        self.keyBox = ComboboxContext(self, font=self.font)
        self.methodBox = ttk.Combobox(self, font=self.font, values=self.__apiMethods, state="readonly")
        #Set default value for method Combobox
        self.methodBox.set(self.__apiMethods[0])
        # Set bind value selection methodCombobox on URL label
        self.methodBox.bind("<<ComboboxSelected>>", self.method_selected)
        self.orgBox.bind("<<ComboboxSelected>>", self.org_selected)
        self.keyBox.bind("<<ComboboxSelected>>", self.key_selected)

        #Buttons
        self.dbAppendBtn = tk.Button(self, text="Добавить в справочник ключ", font=self.font,
                                     command=UIMain.create_window)
        bold_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.sendRequestBtn = tk.Button(self, text="Выполнить", font=bold_font, command=self.send_request)

        self.searchPhoto = tk.PhotoImage(file=r"search.png").subsample(2,2)
        self.searchBtn = tk.Button(self, text="Найти", image=self.searchPhoto, command=self.search_res)
        self.searchBtn.image = self.searchPhoto

        self.refreshPhoto = tk.PhotoImage(file=r"refresh.png")
        self.refreshBtn = tk.Button(self, image=self.refreshPhoto, command=self.refresh)
        self.refreshBtn.image = self.refreshPhoto

        #Text boxes
        self.jsonRequestBox = TextContext(self, height=50, font=self.font,
                                          wrap="none")
        self.jsonTipsBox = TextContext(self, width=30, height=30, font=self.font, wrap="none", state="disabled")
        self.jsonResponseBox = TextContext(self, width=30, height=30, font=self.font, wrap="none", state="disabled")

        loggerUI.info("Main window objects initialized")

        self.widgets_place()

    #Define search function text
    def search_res(self):
        loggerUI.info("Click on search button")
        self.jsonResponseBox.tag_remove('found', '1.0', "end")
        src = self.searchEntry.get()
        if src:
            idx = '1.0'
            while 1:
                idx = self.jsonResponseBox.search(src, idx, nocase=False, stopindex="end")
                if not idx: break
                last_idx = '%s+%dc' % (idx, len(src))
                self.jsonResponseBox.tag_add('found', idx, last_idx)
                idx = last_idx
                self.jsonResponseBox.see(idx)
            self.jsonResponseBox.tag_config('found', foreground='red')
            loggerUI.info(f"Search the text '{self.searchEntry.get()}' complete")
        self.searchEntry.focus_set()

    #Supporting function changing text boxes on refresh data
    def insert_json_and_hint(self, key, url):
        db_client = MongoDB()
        self.jsonRequestBox.delete("1.0", "end")
        self.jsonRequestBox.insert("0.0", db_client.load_json(key, url))
        self.jsonTipsBox["state"] = "normal"
        self.jsonTipsBox.delete("1.0", "end")
        self.jsonTipsBox.insert("0.0", db_client.load_hint(key, url))
        self.jsonTipsBox["state"] = "disabled"
        db_client.close()

    # Function for refresh button
    def refresh(self):
        loggerUI.info("Click on refresh button")
        try:
            db_client = MongoDB()
            api_keys = db_client.load_keys()
            self.keyBox["values"] = [key for key in api_keys.keys()]
            self.orgBox["values"] = [name for name in api_keys.values()]
            url_method = self.__url_dict[self.methodBox.get()]
            key = self.keyBox.get()
            db_client.close()
            if key and len(key) >= 8:
                self.insert_json_and_hint(key, url_method)
            self.jsonStatusLabel["text"] = "Data refreshed"
            self.jsonStatusLabel["fg"] = "green"
            loggerUI.info("Refresh complete, data loaded")
        except pymongo.errors.AutoReconnect:
            self.jsonStatusLabel["text"] = "Error Connection"
            self.jsonStatusLabel["fg"] = "red"

    # Function on api key box selected
    def key_selected(self, event):
        loggerUI.info("Combobox api key changed. Try to process refreshing data")
        db_client = MongoDB()
        key = self.keyBox.get()
        api_keys = db_client.load_keys()
        self.orgBox.set(api_keys[key])
        url_method = self.__url_dict[self.methodBox.get()]
        if key and len(key) >= 8:
            self.insert_json_and_hint(key, url_method)
        self.jsonStatusLabel["text"] = "Data refreshed"
        self.jsonStatusLabel["fg"] = "green"
        db_client.close()
        loggerUI.info("Refresh complete, data loaded")

    # Function on org name box selected
    def org_selected(self, event):
        loggerUI.info("Combobox orgname changed. Try to process refreshing data")
        db_client = MongoDB()
        name = self.orgBox.get()
        api_keys = db_client.load_keys()
        db_client.close()
        keys = [key for key in api_keys if api_keys[key] == name]
        if keys:
            self.keyBox.set(keys[0])
        key = self.keyBox.get()
        if key and len(key) >= 8:
            url_method = self.__url_dict[self.methodBox.get()]
            self.insert_json_and_hint(key, url_method)



    # Select function for binding on selection Combobox
    def method_selected(self, event):
        loggerUI.info("Method combobox changed")
        selection = self.methodBox.get()
        self.urlLabel["text"] = f"URL: {self.__url_dict[selection]}"
        key = self.keyBox.get()
        if key and len(key) >= 8:
            self.insert_json_and_hint(key, self.__url_dict[selection])
            loggerUI.info("method Combobox changed got refresh json and hint")
        else:
            loggerUI.info("method Combobox doesn't change data, because valid api key is missing")


    # Search function for binding event and logging
    def search_res_ev(self, event):
        self.search_res()
        if self.searchEntry.get():
            loggerUI.info(f"Key 'Enter' pressed and search started with text '{self.searchEntry.get()}'")
        else:
            loggerUI.info("Key 'Enter' pressed and search started with empty text")

    # Search function for without binding event and logging
    def search_btn_click(self):
        self.search_res()
        if self.searchEntry.get():
            loggerUI.info(f"Button 'Найти' pressed and search started with text '{self.searchEntry.get()}'")
        else:
            loggerUI.info("Button 'Найти' pressed and search started with empty text")

    # Function that places objects initialized earlier
    def widgets_place(self):
        self.orgLabel.place(x=2, y=3, width=80)
        self.orgBox.place(x=80, y=3, relwidth=0.4)
        self.keyLabel.place(x=2, y=26, width=80)
        self.keyBox.place(x=80, y=26, relwidth=0.4)
        self.methodLabel.place(x=2, y=49, width=80)
        self.methodBox.place(x=80, y=49, relwidth=0.4)
        self.dbAppendBtn.place(x=2, y=71, width=185)
        self.sendRequestBtn.place(x=187, y=71, width=100, height=28)
        self.refreshBtn.place(x=287, y=71, width=28, height=28)
        self.urlLabel.place(x=2, y=97, width=450)
        self.jsonRequestLabel.place(x=2, y=115, width=38)
        self.jsonRequestBox.place(x=2, y=135, relwidth=0.37, relheight=0.8)
        self.jsonTipsBox.place(relx=0.37, y=135, relwidth=0.25, relheight=0.8)
        self.jsonTipsLabel.place(relx=0.37, y=115, width=121)
        self.jsonStatusLabel.place(relx=0.7, y=3, relwidth=0.3, height=55)
        self.jsonResponseLabel.place(relx=0.7, y=60, relwidth=0.3)
        self.jsonResponseBox.place(relx=0.62, y=105, relwidth=0.378, relheight=0.83)
        self.searchEntry.place(relx=0.62, y=80, relwidth=0.3, height=28)
        self.searchBtn.place(relx=0.92, y=80, width=28, height=28)

        loggerUI.info("Initialized objects placed on main window successfully")

    # Main function that sending api request on a clicking button
    def send_request(self):
        self.jsonResponseBox["state"] = "normal"
        loggerUI.info("Click button 'Выполнить'")
        self.jsonResponseBox.delete("1.0", "end")
        apikey = self.keyBox.get()
        loggerUI.info(f"got APIkey from box: {apikey}")
        if not apikey or len(apikey) < 8:
            self.jsonResponseBox.insert("0.0", "Введите валидный API key")
            loggerUI.info(f"Invalid API key")
            self.jsonStatusLabel["fg"] = "red"
            self.jsonStatusLabel["text"] = "Value error"
        else:
            url = self.__url_dict[self.methodBox.get()]
            if not self.jsonRequestBox.compare("end-1c", "==", "1.0"):
                data = self.jsonRequestBox.get("1.0", "end")
            else:
                data = "{}"
            loggerUI.info(f"got json data from json box: \n{data} and try sending request")
            request = APITrnRequest(apikey, url=url, data=data)
            response_code, response = request.post()
            try:
                db_client = MongoDB()
                db_client.insert_json(apikey, url, data)
                db_client.insert_hint(apikey, url)
                db_client.close()
            except pymongo.errors.AutoReconnect:
                loggerDB.error("Connection error to MongoDB. Request data will saved after reconnect.")
                loggerUI.error("Connection error to MongoDB. Request data will saved after reconnect. App data might display incorrectly")
            self.jsonStatusLabel["text"] = f"Status: {response_code}"
            if response_code == 200:
                self.jsonStatusLabel["fg"] = "green"
            else:
                self.jsonStatusLabel["fg"] = "red"
            self.jsonResponseBox.insert("0.0", response)
            loggerUI.info("Request compeleted and set on text box")
            self.insert_json_and_hint(apikey, url)
            loggerUI.info("Data on form refreshed after request")
        self.jsonResponseBox["state"] = "disabled"


    def __del__(self):
        loggerUI.info("Main window closed and application stopped")
