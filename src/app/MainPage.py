from tkinter import *
from tkinter import ttk
from .IPage import IPage
from .CheckoutPage import CheckoutPage
from .SettingsPage import SettingsPage
from .ManagePage import ManagePage
from core.GitManager import *



class MainPage(IPage):



    def __init__(self, parent, controller, git_manager, logger):
        super().__init__(parent, logger)
        self.git_manager = git_manager
        self.repo_name = Label(self)
        self.repo_name.grid(column=1, row=1)
        self.action_text = Label(self, text="What would you like to do?")
        self.action_text.grid(column=1, row=2)
        self.checkout_project_button = Button(self, text="Checkout Project", command=lambda: controller.show_frame(CheckoutPage))
        self.checkout_project_button.grid(column=1, row=3)
        self.manage_project_button = Button(self, text="Manage Project", command=lambda: controller.show_frame(ManagePage))
        self.manage_project_button.grid(column=1, row=4)
        self.settings_button = Button(self, text="Settings", command=lambda: controller.show_frame(SettingsPage))
        self.settings_button.grid(column=1, row=5)
        self.pad()



    def post_raise(self):
        self.repo_name.config(text=(
            f'Checked Out: {"None" if not self.git_manager.repo else self.git_manager.repo_name + " (" + self.git_manager.repo.active_branch.name + ")"}'
            ))
