from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from .IPage import IPage
from core.GitManager import *



class PublishPage(IPage):



    def __init__(self, parent, controller, git_manager, logger):
        
        super().__init__(parent, logger)

        self.git_manager = git_manager
        
        self.path_url_text = Label(self, text="Path")
        self.path_url_text.grid(column=0, row=1)
        self.path_stringvar = StringVar()
        self.path_stringvar = StringVar()
        self.path_stringvar.trace_add("write", self.verify_local)
        self.path_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH, textvariable=self.path_stringvar)
        self.path_entry.grid(column=1, row=1)
        self.browse_button = Button(self, text="Browse 🗀", command=self.browse)
        self.browse_button.grid(column=2, row=1)
        
        self.message_text = Label(self, text="Message")
        self.message_text.grid(column=0, row=2)
        self.message_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH)
        self.message_entry.grid(column=1, row=2)
        self.publish_button = Button(self, text="Publish", command=self.publish)
        self.publish_button.grid(column=2, row=2)

        self.back_button = Button(self, text="Back", command=lambda: controller.go_home())
        self.back_button.grid(column=0, row=3, padx=IPage.GRID_PADDING, pady=IPage.GRID_PADDING)

        self.add_info_message(1,3)
        self.pad()



    def verify_local(self, *args):
        path = self.path_stringvar.get()
        if is_local_repository(path):
            self.message_entry.config(state='normal')
            self.publish_button.config(state='normal')
            self.logger.info(f'Path {path} is a verified local repository. Ready to publish.')
        else:
            self.message_entry.config(state='disabled')
            self.publish_button.config(state='disabled')
            self.logger.info(f'Path {path} is NOT a local repository. Blocking publish until path points to local git repo.')
            self.set_message('Path does not point to valid local Git repository!', 'error')
        # TODO app message to display that a local repo is being used instead of remote
        # TODO maybe debounce so that the log isn't polluted with each change to the stringvar. currently its every single character change



    def publish(self):
        path = self.path_stringvar.get()
        message = self.message_entry.get()
        self.logger.info(f'Attempting to publish from local repo {path}')

        if not message:
            self.logger.warning(f'Rejecting publish due to lack of commit message.')
            self.set_message(f'Cannot publish without a message!', 'warning')
            return
        
        if not is_local_repository(path):
            self.logger.error(f'Failed. {path} is not a valid local repo.')
            self.set_message('Path does not point to valid local repo!', 'error')
            return
        
        if not self.git_manager.is_dirty():
            self.logger.error(f'No changes to publish. Aborting.')
            self.set_message('This repository has no changes to publish.', 'warning')
            return
        
        if not self.git_manager.commission_branch_checked_out():
            self.logger.error(f'Failed. There are changes, but not in a commission branch. Corrupt project state.')
            self.set_message('Repository corrupted. Reach out to programmer or Carter Dugan.', 'error')
            return
        
        try:
            self.git_manager.add_changes()
            self.git_manager.commit_changes(message)
            self.git_manager.push_changes()
            self.git_manager.checkout_default_branch()
            self.set_message('Published! Checkout the project again before making more changes.', 'success')
        except Exception as e:
            self.logger.error(f'Fatal Git error: {e}')
            self.set_message('FATAL: Git error. Contact programmer or Carter Dugan', 'error')


    
    def browse(self):
        self.logger.info('Browsing local files for publish path.')
        folder_path = askdirectory()
        self.logger.info(f'User selected path: "{folder_path}" for publish.')
        self.path_stringvar.set(folder_path)
