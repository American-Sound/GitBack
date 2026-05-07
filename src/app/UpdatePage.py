from tkinter import *
from tkinter import ttk
from .IPage import IPage
from .MainPage import MainPage
from core.GitManager import *
from core.Updater import *
import sys



class UpdatePage(IPage):



    def __init__(self, parent, controller, git_manager, logger):
        super().__init__(parent, logger)
        self.available_updates = check_for_update()
        self.action_text = Label(self, text="Updates available!")
        self.action_text.grid(column=1, row=1)
        self.checkout_project_button = Button(self, text="Close and Update", command=self.update)
        self.checkout_project_button.grid(column=1, row=2, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)
        self.publish_project_button = Button(self, text="Ignore", command=lambda: controller.show_frame(MainPage))
        self.publish_project_button.grid(column=1, row=3, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)
        self.pad()


    
    def updates_available(self):
        return self.available_updates != None



    def update(self):
        self.logger.info('Attempting to update...')
        try:
            url = get_download_url(self.available_updates)
            path = download_update(url)
            apply_update(path)
        except:
            self.logger.exception('Failed with the following error:')
            sys.exit()
