from tkinter import font as tkfont
import tkinter as tk
import tkinter.ttk as ttk
import logging

#   Set logging module UI.py

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


#   Define class for dialog window that adds data to DB
class DialogWindow(tk.Toplevel):
    def __init__(self, form_name="Добавить API ключ", form_size="400x90", font=ui_font):
        # Init objects for dialog window
        super().__init__()
        self.font = font
        self.title(form_name)
        self.resizable(False, False)
        self.geometry(form_size)

        self.orgLabel = tk.Label(self, text="Название", font=self.font, anchor="w")
        self.keyLabel = tk.Label(self, text="API ключ", font=self.font, anchor="w")
        self.orgBox = ttk.Combobox(self, font=self.font)
        self.keyBox = ttk.Combobox(self, font=self.font)
        self.dbAppendBtn = tk.Button(self, text="Добавить", font=self.font)

        loggerUI.info("Dialog window objects initialized")

        self.widgets_place()

    # Function that places objects initialized earlier
    def widgets_place(self):
        self.orgLabel.place(x=2, y=3, width=80)
        self.orgBox.place(x=80, y=3, width=300)
        self.keyLabel.place(x=2, y=26, width=80)
        self.keyBox.place(x=80, y=26, width=300)
        self.dbAppendBtn.place(x=2, y=48, width=140)
        loggerUI.info("Initialized objects placed on dialog window successfully")

    def dismiss(self):
        self.grab_release()
        self.destroy()
        loggerUI.info("Dialog window closed")

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

    def __init__(self, form_name="Test", form_size="1024x768", font=ui_font):
        super().__init__()

        #  Initialize attributes of main window
        self.title(form_name)
        #self.resizable(False, False)
        self.geometry(form_size)
        self.font = font
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
        self.jsonResponseLabel = tk.Label(self, text="JSON Ответ", font=self.font, anchor="e")
        self.urlLabel = tk.Label(self, text="URL: https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_status",
                                  font=self.font, anchor="w")

        #Drop lists (Comboboxes)
        self.orgBox = ttk.Combobox(self, font=self.font)
        self.keyBox = ttk.Combobox(self, font=self.font)
        self.methodBox = ttk.Combobox(self, font=self.font, values=self.__apiMethods)

        #Buttons
        self.dbAppendBtn = tk.Button(self, text="Добавить в справочник ключ", font=self.font, command=UIMain.create_window)
        bold_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.sendRequestBtn = tk.Button(self, text="Выполнить", font=bold_font)

        #Text boxes
        self.jsonRequestBox = TextContext(self, height = 50, font=self.font,
                                            wrap="none")
        self.jsonTipsBox = TextContext(self, width=30, height = 30, font=self.font, wrap="none", state="disabled")
        self.jsonResponseBox = TextContext(self, width=30, height = 30, font=self.font, wrap="none")

        loggerUI.info("Main window objects initialized")

        self.widgets_place()


        #Function that places objects initialized earlier
    def widgets_place(self):
        self.orgLabel.place(x=2, y=3, width=80)
        self.orgBox.place(x=80, y=3, relwidth=0.4)
        self.keyLabel.place(x=2, y=26, width=80)
        self.keyBox.place(x=80, y=26, relwidth=0.4)
        self.methodLabel.place(x=2, y=49, width=80)
        self.methodBox.place(x=80, y=49, relwidth=0.4)
        self.dbAppendBtn.place(x=2, y=71, width=185)
        self.sendRequestBtn.place(x=187, y=71, width=100, height = 28)
        self.urlLabel.place(x=2, y=97, width=450)
        self.jsonRequestLabel.place(x=2, y=115, width=38)
        self.jsonRequestBox.place(x=2, y=135, relwidth=0.37, relheight=0.8)
        self.jsonTipsBox.place(relx=0.37, y=135, relwidth=0.25, relheight=0.8)
        self.jsonTipsLabel.place(relx=0.37, y=115, width=121)
        self.jsonStatusLabel.place(relx=0.7, y=3, relwidth=0.3, height=55)
        self.jsonResponseLabel.place(relx=0.7, y=60, relwidth=0.3)
        self.jsonResponseBox.place(relx=0.62, y=80, relwidth=0.378, relheight=0.86)
        loggerUI.info("Initialized objects placed on main window successfully")

    def __del__(self):
        loggerUI.info("Main window closed and application stopped")



