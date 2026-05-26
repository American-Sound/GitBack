from tkinter import *
from tkinter import ttk
from .IPage import IPage
from .CheckoutPage import CheckoutPage
from .PublishPage import PublishPage
from core.GitManager import *



class SettingsPage(IPage):



    def __init__(self, parent, controller, git_manager, logger):
        
        super().__init__(parent, logger)

        self.git_manager = git_manager

        config = self.git_manager.get_global_config()
        
        self.user_name_text = Label(self, text="User Name")
        self.user_name_text.grid(column=0, row=1)
        self.user_name_stringvar = StringVar(value=config['user.name'])
        self.user_name_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH, textvariable=self.user_name_stringvar)
        self.user_name_entry.grid(column=1, row=1)
        
        self.user_email_text = Label(self, text="User Email")
        self.user_email_text.grid(column=0, row=2)
        self.user_email_stringvar = StringVar(value=config['user.email'])
        self.user_email_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH, textvariable=self.user_email_stringvar)
        self.user_email_entry.grid(column=1, row=2)
        
        self.save_button = Button(self, text="Save Settings", command=self.save_settings)
        self.save_button.grid(column=1, row=4)

        self.back_button = Button(self, text="Back", command=lambda: controller.go_home())
        self.back_button.grid(column=0, row=4, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)

        self.add_info_message(1,3)
        self.pad()



    def save_settings(self):
        config= {
            'user.name'     : self.user_name_stringvar.get(),
            'user.email'    : self.user_email_stringvar.get(),
            'core.autocrlf' : True
        }
        
        self.logger.info(f'Attempting to save the following settings: {config}')
        
        try:
            self.git_manager.set_global_config(config)
            self.set_message('Settings saved!', 'success')
        except:
            self.set_message('ERROR: Settings could not be saved.', 'error')
        
        self.validate_credentials()        
    


    def validate_credentials(self) -> bool:
        if not self.git_manager.valid_global_config():
            self.set_message('Please set your credentials!', 'warning')
            self.back_button.config(state='disabled')
        else:
            self.back_button.config(state='normal')

