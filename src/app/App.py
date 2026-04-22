from tkinter import *
from tkinter import ttk
from .MainPage import MainPage
from .CheckoutPage import CheckoutPage
from .PublishPage import PublishPage



class App(Tk):
    


    def __init__(self, git_manager, logger):
        super().__init__()
        container = Frame(self)
        self.title("GitBack")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, CheckoutPage, PublishPage):
            frame = F(container, self, git_manager, logger)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(MainPage)

    def go_home(self):
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update_idletasks()
        self.geometry(f"{frame.winfo_reqwidth()}x{frame.winfo_reqheight()}")
