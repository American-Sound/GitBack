from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time



class IPage(Frame):



    # Magic Numbers

    ## App dimensions
    GRID_PADDING: int             = 5
    MAINFRAME_PADDING_X: int      = 12
    MAINFRAME_PADDING_Y: int      = 3

    ## Text entry boxes
    TEXT_ENTRY_WIDTH: int = 60

    ## user messages/warnings
    WARNING_LIFETIME: int = 5

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

        logo_image = Image.open('res/logo.png').resize((self.LOGO_WIDTH, self.LOGO_HEIGHT))
        self.logo = ImageTk.PhotoImage(logo_image)
        self.logo_label = Label(self, image=self.logo)
        self.logo_label.image = self.logo
        self.logo_label.grid(column=1, row=0, padx=self.MAINFRAME_PADDING_X, pady=self.MAINFRAME_PADDING_Y)

        self.logger = logger

        self.message = None

    

    def add_info_message(self, p_column, p_row):
        self.message_stringvar = StringVar()
        self.message = Label(self, textvariable=self.message_stringvar)
        self.message.grid(column=p_column, row=p_row, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)
        self.message_lock = threading.Lock()



    def set_message(self, message, severity='info'):
        if not self.message: return

        if severity == 'info':
            self.message.config(foreground='Black')
        elif severity == 'warning':
            self.message.config(foreground='#A0A000')
        elif severity == 'error':
            self.message.config(foreground='Red')
        elif severity == 'success':
            self.message.config(foreground='Green')

        thread = threading.Thread(target=self._set_temporary_message, args=(message,))
        thread.start()


    
    def _set_temporary_message(self, message):
        if not self.message: return

        # try-catch here because if the user closes the window before the thread resumes,
        # we get a runtime error. Should not add anything else to this try: block.
        try:
            with self.message_lock:
                for i in range(self.WARNING_LIFETIME):
                    self.message_stringvar.set(message + f' ({self.WARNING_LIFETIME - i}s)')
                    time.sleep(self.WARNING_LIFETIME / self.WARNING_LIFETIME)
                self.message_stringvar.set('')
        except RuntimeError:
            pass


    def pad(self):
        def _pad_all(widget):
            for child in widget.winfo_children():
                child.grid_configure(padx=self.GRID_PADDING, pady=self.GRID_PADDING)
                _pad_all(child)
        _pad_all(self)
