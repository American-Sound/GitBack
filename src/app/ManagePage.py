from tkinter import *
from tkinter import ttk
from .IPage import IPage
from core.GitManager import *
import re



class ManagePage(IPage):



    def __init__(self, parent, controller, git_manager, logger):

        super().__init__(parent, logger)

        self.git_manager = git_manager

        self.repo_text = Label(self, text="Checked Out:")
        self.repo_text.grid(column=0, row=1)
        self.repo_name = Label(self)
        self.repo_name.grid(column=1, row=1, sticky='w')

        self.branch_text = Label(self, text="Working Branch:")
        self.branch_text.grid(column=0, row=2)
        self.branch_dropdown = ttk.Combobox(self, width=IPage.DROPDOWN_WIDTH)
        self.branch_dropdown.grid(column=1, row=2, sticky='w')
        self.branch_dropdown.bind('<<ComboboxSelected>>', self.change_branch)

        self.new_branch_text = Label(self, text="New Branch:")
        self.new_branch_text.grid(column=0, row=3)
        self.new_branch_stringvar = StringVar()
        self.new_branch_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH, textvariable=self.new_branch_stringvar)
        self.new_branch_entry.grid(column=1, row=3)
        self.new_branch_button = Button(self, text="New Branch", command=self.new_branch)
        self.new_branch_button.grid(column=2, row=3)

        self.message_text = Label(self, text="Snapshot Message")
        self.message_text.grid(column=0, row=4)
        self.save_message_stringvar = StringVar()
        self.save_message_entry = Entry(self, width=IPage.TEXT_ENTRY_WIDTH, textvariable=self.save_message_stringvar)
        self.save_message_entry.grid(column=1, row=4)
        self.save_button = Button(self, text="Save Snapshot", command=self.save_snapshot)
        self.save_button.grid(column=2, row=4)

        self.publish_button = Button(self, text="Publish", command=self.publish_project)
        self.publish_button.grid(column=2, row=5)

        self.add_info_message(1,6)
        self.add_home_button(0,6,controller)
        self.pad()



    def post_raise(self):
        self.validate_project_state()
        self.repo_name.config(text=(
            f'{"None" if not self.git_manager.repo else self.git_manager.repo_name + " (" + self.git_manager.repo.active_branch.name + ")"}'
            ))
        self.branch_dropdown.set('' if not self.git_manager.repo else self.git_manager.repo.active_branch.name)



    def validate_project_state(self):
        can_change_branch = True
        if not self.git_manager.is_project_checked_out():
            interactive_state = 'disabled'
            can_change_branch = False
            self.set_message('No project checked out!', 'warning')
        elif self.git_manager.default_branch_checked_out():
            interactive_state = 'disabled'
            self.set_message('You must checkout a commission branch!', 'warning')
        else:
            interactive_state = 'normal'
            self.clear_message()
        if self.git_manager.repo:
            self.branch_dropdown.config(values=self.git_manager.get_commission_branches())
        self.message_text.config(state=interactive_state)
        self.save_message_entry.config(state=interactive_state)
        self.save_button.config(state=interactive_state)
        self.publish_button.config(state=interactive_state)

        self.branch_text.config(state='normal' if can_change_branch else 'disabled')
        self.branch_dropdown.config(state='normal' if can_change_branch else 'disabled')
        self.new_branch_text.config(state='normal' if can_change_branch else 'disabled')
        self.new_branch_entry.config(state='normal' if can_change_branch else 'disabled')
        self.new_branch_button.config(state='normal' if can_change_branch else 'disabled')



    def save_snapshot(self):
        message = self.save_message_entry.get()
        self.logger.info(f'Attempting to commit to local repo')

        if not message:
            self.logger.warning(f'Rejecting commit due to lack of commit message.')
            self.set_message(f'Cannot save without a message!', 'warning')
            return

        if not self.git_manager.is_dirty():
            self.logger.error(f'No changes to commit. Aborting.')
            self.set_message('This repository has no changes to save.', 'warning')
            return

        if not self.git_manager.commission_branch_checked_out():
            self.logger.error(f'Failed. There are changes, but not in a commission branch. Corrupt project state.')
            self.set_message('Repository corrupted. Reach out to programmer or Carter Dugan.', 'error')
            return

        self.git_manager.add_changes()
        self.git_manager.commit_changes(message)
        self.logger.info('Successfully save snapshot!')
        self.set_message('Snapshot saved!', 'success')


    def publish_project(self):
        if (self.git_manager.is_dirty()):
            self.logger.warning(f'Rejecting publish due to uncommitted changes.')
            self.set_message('Project has unsaved changes! Aborting.', 'error')
            return
        try:
            self.git_manager.push_changes()
            self.git_manager.checkout_default_branch()
            self.set_message('Published!', 'success')
        except Exception:
            self.logger.exception(f'Fatal Git error:')
            self.set_message('FATAL: Git error. Contact programmer or Carter Dugan', 'error')


    def change_branch(self, *args):
        branch = self.branch_dropdown.get()
        self.logger.info(f'Attempting to checkout branch {branch} from dropdown...')
        if self.git_manager.is_dirty():
            self.logger.error(f'Failed to checkout existing branch {branch} due to existing changes without a snapshot.')
            self.set_message('Branch has unsaved changes! Aborting.', 'error')
            return
        try:
            self.git_manager.checkout_default_branch()
            self.git_manager.pull_updates()
            self.git_manager.checkout_branch(branch)
            self.post_raise()
            self.set_message(f'Switched to {branch}')
        except:
            self.logger.exception(f'Fatal Git error:')
            self.set_message('FATAL: Git error. Contact programmer or Carter Dugan', 'error')



    def new_branch(self, *args):
        branch = 'commission-branch-' + self.new_branch_stringvar.get()
        if re.search(r'[^a-zA-Z0-9._\-/]', branch):
            self.logger.error(f'Failed to checkout new commission branch due to invalid characters "{branch}"')
            self.set_message('Invalid characters. Can only use numbers, letters, and ._-/')
            return

        if self.git_manager.is_dirty():
            self.logger.error(f'Failed to checkout new branch {branch} due to existing changes without a snapshot.')
            self.set_message('Branch has unsaved changes! Aborting.', 'error')
            return

        try:
            self.git_manager.checkout_default_branch()
            self.git_manager.pull_updates()
            self.git_manager.checkout_new_branch(branch)
            self.post_raise()
            self.set_message(f'Switched to {branch}')
        except:
            self.logger.exception(f'Fatal Git error:')
            self.set_message('FATAL: Git error. Contact programmer or Carter Dugan', 'error')
