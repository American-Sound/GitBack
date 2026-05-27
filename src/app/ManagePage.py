from tkinter import *
from tkinter import ttk
from .IPage import IPage
from core.GitManager import *



class ManagePage(IPage):



    def __init__(self, parent, controller, git_manager, logger):

        super().__init__(parent, logger)

        self.git_manager = git_manager

        # self.add_info_message(1,3)
        self.pad()
        self.validate_project_state()




    def validate_project_state(self):
        # TODO
        pass
