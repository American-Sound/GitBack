import git
from git import Git, GitCommandError
import logging
from pathlib import Path
import threading



def is_local_repository(path):
    directory = Path(path)
    return (directory / '.git').is_dir()



def is_remote_repository(url):
    try:
        Git().execute(['git', 'ls-remote', url])
        return True
    except GitCommandError:
        return False



class GitManager:



    def __init__(self, logger : logging.Logger):
        self.logger = logger
        self.config = git.GitConfigParser()
        self.repo = None
        self.commission_number = 0
        self.lock = threading.Lock()
    


    def is_dirty(self):
        return self.repo.is_dirty(untracked_files=True)



    def default_branch_checked_out(self):
        return self.repo.active_branch.name in ('main', 'master')
    


    def commission_branch_checked_out(self):
        return self.repo.active_branch.name.startswith('commission-branch-')


    
    def pull_updates(self):
        self.repo.git.pull()


    
    def checkout_commission_branch(self):
        while 'origin/commission-branch-' + str(self.commission_number) in [ref.name for ref in self.repo.remote().refs]:
            self.commission_number += 1    
        self.repo.create_head('commission-branch-' + str(self.commission_number)).checkout()
    


    def checkout_default_branch(self):
        if 'origin/main' in [ref.name for ref in self.repo.remote().refs]:
            self.repo.heads['main'].checkout()
        else:
            self.repo.heads['master'].checkout()


    
    def checkout_local_repo(self, path):
        self.repo = git.Repo(path)



    def clone_project(self, url, path):
        self.repo = git.Repo.clone_from(url, path)
        self.logger.info(f'Successfully cloned {url} to {path}')



    def add_changes(self):
        self.repo.index.add(['*'])
    


    def commit_changes(self, message):
        self.repo.index.commit(message)


    
    def push_changes(self):
        self.repo.remote().push(refspec=('commission-branch-' + str(self.commission_number)))
