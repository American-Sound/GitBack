from tkinter import *
from tkinter import ttk
from .IPage import IPage
from .CheckoutPage import CheckoutPage
from .PublishPage import PublishPage
from core.GitManager import *



class MainPage(IPage):

    def __init__(self, parent, controller, git_manager, logger):
        super().__init__(parent, logger)
        self.action_text = Label(self, text="What would you like to do?")
        self.action_text.grid(column=1, row=1)
        self.checkout_project_button = Button(self, text="Checkout Project", command=lambda: controller.show_frame(CheckoutPage))
        self.checkout_project_button.grid(column=1, row=2, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)
        self.publish_project_button = Button(self, text="Publish Project", command=lambda: controller.show_frame(PublishPage))
        self.publish_project_button.grid(column=1, row=3, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)
        self.pad()
