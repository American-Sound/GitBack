from tkinter import *
from tkinter import ttk
from .IPage import IPage
from .CheckoutPage import CheckoutPage
from .PublishPage import PublishPage
from .SettingsPage import SettingsPage
from core.GitManager import *



class MainPage(IPage):



    def __init__(self, parent, controller, git_manager, logger):
        super().__init__(parent, logger)
        self.action_text = Label(self, text="What would you like to do?")
        self.action_text.grid(column=1, row=1)
        self.checkout_project_button = Button(self, text="Checkout Project", command=lambda: controller.show_frame(CheckoutPage))
        self.checkout_project_button.grid(column=1, row=2)
        self.publish_project_button = Button(self, text="Publish Project", command=lambda: controller.show_frame(PublishPage))
        self.publish_project_button.grid(column=1, row=3)
        self.settings_button = Button(self, text="Settings", command=lambda: controller.show_frame(SettingsPage))
        self.settings_button.grid(column=1, row=4)
        self.pad()
