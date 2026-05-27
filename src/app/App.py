from tkinter import *
from tkinter import ttk
from .MainPage import MainPage
from .CheckoutPage import CheckoutPage
from .PublishPage import PublishPage
from .UpdatePage import UpdatePage
from .SettingsPage import SettingsPage
from .ManagePage import ManagePage
from core.Updater import *



class App(Tk):



    def __init__(self, git_manager, logger):
        super().__init__()
        container = Frame(self)
        self.git_manager = git_manager
        self.title("GitBack")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames_stack = []

        for F in (UpdatePage, MainPage, CheckoutPage, ManagePage, PublishPage, SettingsPage):
            frame = F(container, self, git_manager, logger)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        if self.frames[UpdatePage].updates_available():
            self.show_frame(UpdatePage)
        else:
            self.go_home()



    def go_home(self):
        # Enforce minimum required configuration
        if not self.git_manager.valid_global_config():
            self.show_frame(SettingsPage)
        else:
            self.show_frame(MainPage)



    def frame_history_populated(self):
        return len(self.frames_stack) > 1



    def go_back(self):
        if len(self.frames_stack) > 1:
            self.frames_stack.pop()
            self.show_frame(frames_stack[-1])



    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.post_raise()
        frame.update_idletasks()
        self.geometry(f"{frame.winfo_reqwidth()}x{frame.winfo_reqheight()}")
        self.frames_stack.append(frame)
