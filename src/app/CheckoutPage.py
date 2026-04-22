from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from .IPage import IPage
from core.GitManager import *



class CheckoutPage(IPage):
    
    
    
    def __init__(self, parent, controller, git_manager, logger):
        
        super().__init__(parent, logger)

        self.git_manager = git_manager
        
        self.repo_url_text = Label(self, text="Repo URL")
        self.repo_url_text.grid(column=0, row=1)
        self.repo_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH)
        self.repo_entry.grid(column=1, row=1)
        self.repo_checkout_button = Button(self, text="Checkout", command=self.checkout)
        self.repo_checkout_button.grid(column=2, row=1)
        
        self.path_text = Label(self, text="Path")
        self.path_text.grid(column=0, row=2)
        self.path_stringvar = StringVar()
        self.path_stringvar.trace_add("write", self.decide_local_or_remote)
        self.path_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH, textvariable=self.path_stringvar)
        self.path_entry.grid(column=1, row=2)
        self.browse_button = Button(self, text="Browse 🗀", command=self.browse)
        self.browse_button.grid(column=2, row=2)

        self.back_button = Button(self, text="Back", command=lambda: controller.go_home())
        self.back_button.grid(column=0, row=3, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)

        self.add_info_message(1,3)
        self.pad()



    def decide_local_or_remote(self, *args):
        path = self.path_stringvar.get()
        if is_local_repository(path):
            self.repo_entry.config(state='disabled')
            self.logger.info(f'Path {path} is a local repository, disabling URL and the local will be used instead.')
            self.set_message('Path points to existing local repo. URL will not be used.', 'warning')
        else:
            self.repo_entry.config(state='normal')
            self.logger.info(f'Path {path} is NOT a local repository. The remote URL will be used for checkout into the specified path.')
        # TODO app message to display that a local repo is being used instead of remote
        # TODO maybe debounce so that the log isn't polluted with each change to the stringvar. currently its every single character change



    def checkout(self):
        path = self.path_stringvar.get()
        url = self.repo_entry.get()
        self.logger.info(f'Attempting to checkout project with path {path} and URL {url}')

        try:
            if is_local_repository(path):
                self.git_manager.checkout_local_repo(path)
                if not self.git_manager.default_branch_checked_out():
                    self.logger.error(f'Failed. Default branch must be checked out, and it is not.')
                    self.set_message('Unpublished changes in this local repository!', 'error')
                    return
                else:
                    self.git_manager.pull_updates()
            else:
                if not is_remote_repository(url):
                    self.logger.error(f'Failed. {url} is not a valid remote repository.')
                    self.set_message('URL does not point to a valid remote repository!', 'error')
                    return
                else:
                    self.git_manager.clone_project(url, path)
            self.git_manager.checkout_commission_branch()
            self.set_message('Project successfully checked out!', 'success')
        except Exception as e:
            self.logger.error(f'Fatal Git error: {e}')
            self.set_message('FATAL: Git error. Contact programmer or Carter Dugan', 'error')


    def browse(self):
        self.logger.info('Browsing local files for checkout path.')
        folder_path = askdirectory()
        self.logger.info(f'User selected path: "{folder_path}" for checkout.')
        self.path_stringvar.set(folder_path)
