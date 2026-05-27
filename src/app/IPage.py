from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from core.Resource import resource_path



class IPage(Frame):



    # Magic Numbers

    ## App dimensions
    GRID_PADDING: int             = 5
    MAINFRAME_PADDING_X: int      = 12
    MAINFRAME_PADDING_Y: int      = 3

    ## Box dimensions
    TEXT_ENTRY_WIDTH: int = 60
    DROPDOWN_WIDTH:   int = 30

    ## user messages/warnings
    WARNING_LIFETIME: int = 10

    ## misc
    LOGO_WIDTH: int  = 255
    LOGO_HEIGHT: int = 66



    def __init__(self, parent, logger):
        Frame.__init__(self, parent)
        self.mainframe = ttk.Frame(self, padding=(
            self.MAINFRAME_PADDING_X,
            self.MAINFRAME_PADDING_X,
            self.MAINFRAME_PADDING_Y,
            self.MAINFRAME_PADDING_Y))
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        logo_image = Image.open(resource_path('res/logo.png')).resize((self.LOGO_WIDTH, self.LOGO_HEIGHT))
        self.logo = ImageTk.PhotoImage(logo_image)
        self.logo_label = Label(self, image=self.logo)
        self.logo_label.image = self.logo
        self.logo_label.grid(column=1, row=0, padx=self.MAINFRAME_PADDING_X, pady=self.MAINFRAME_PADDING_Y)

        self.logger = logger

        self.message = None
        self.home_button = None



    def add_info_message(self, p_column, p_row):
        self.message_stringvar = StringVar()
        self.message = Label(self, textvariable=self.message_stringvar)
        self.message.grid(column=p_column, row=p_row, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)
        self.message_lock = threading.Lock()
        self.message_id = 0



    def add_home_button(self, p_column, p_row, controller):
        self.home_button = Button(self, text="Home", command=lambda: controller.go_home())
        self.home_button.grid(column=p_column, row=p_row)



    def set_message(self, message, severity='info'):
        if not self.message: return

        color_map = {'info': 'Black', 'warning': '#808000', 'error': 'Red', 'success': 'Green'}
        color = color_map.get(severity, 'Black')
        self.after(0, lambda: self.message.config(foreground=color))

        with self.message_lock:
            self.message_id += 1
            my_id = self.message_id

        thread = threading.Thread(target=self._set_temporary_message, args=(message, my_id,), daemon=True)
        thread.start()



    def clear_message(self):
        with self.message_lock:
            self.message_id += 1



    # This method is called by the App controller object after a page transition occurs.
    # It can be overridden in child classes order to enforce checks, setup, etc..
    def post_raise(self):
        pass



    def _set_temporary_message(self, message, my_id):
        if not self.message: return
        try:
            for i in range(self.WARNING_LIFETIME):
                with self.message_lock:
                    if self.message_id != my_id:
                        return
                self.after(0, lambda i=i: self.message_stringvar.set(message + f' ({self.WARNING_LIFETIME - i}s)'))
                time.sleep(1)
            with self.message_lock:
                if self.message_id == my_id:
                    self.after(0, lambda: self.message_stringvar.set(''))
        except RuntimeError:
            pass



    def pad(self):
        def _pad_all(widget):
            for child in widget.winfo_children():
                child.grid_configure(padx=self.GRID_PADDING, pady=self.GRID_PADDING)
                _pad_all(child)
        _pad_all(self)
