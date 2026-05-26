import git
from git import Git, GitCommandError, GitConfigParser
import logging
from pathlib import Path
import threading
import platform
import shutil
import os



def is_local_repository(path):
    directory = Path(path)
    return (directory / '.git').is_dir()



def is_remote_repository(url):
    try:
        Git().execute(['git', 'ls-remote', url])
        return True
    except GitCommandError:
        return False



def _setup_git_environment(logger: logging.Logger) -> None:

    logger. info('Setting up Git environment.')
    if platform.system() != 'Windows':
        logger.info('System is not windows, no setup needed for Git')
        return
    
    git_exe = shutil.which('git')
    if not git_exe:
        logger.warning('git.exe not found on PATH; skipping environment setup.')
        return
 
    git_root = Path(git_exe).resolve().parent
    if git_root.name in ('cmd', 'bin'):
        git_root = git_root.parent
    if git_root.name == 'mingw64':
        git_root = git_root.parent
 
    usr_bin   = git_root / 'usr' / 'bin'
    mingw_bin = git_root / 'mingw64' / 'bin'
 
    if not usr_bin.is_dir() or not mingw_bin.is_dir():
        logger.warning(f'Git for Windows layout unexpected at {git_root}; skipping environment setup.')
        return
 
    current_path = os.environ.get('PATH', '')
    new_path = f'{usr_bin};{mingw_bin};{current_path}'
    os.environ['PATH'] = new_path
 
    os.environ.setdefault('MSYSTEM', 'MINGW64')
 
    logger.info(f'Configured git environment from install root: {git_root}')



class GitManager:



    def __init__(self, logger : logging.Logger):
        self.logger = logger
        self.config = git.GitConfigParser()
        _setup_git_environment(logger)
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
        self.repo.git.add(['*'])
    


    def commit_changes(self, message):
        self.repo.git.commit(m=message)


    
    def push_changes(self):
        self.repo.remote().push(refspec=('commission-branch-' + str(self.commission_number)))
    


    def get_global_config(self) -> dict:
        config = {}

        with GitConfigParser(os.path.expanduser('~/.gitconfig'), read_only=True) as cw:
            config['user.name'] = cw.get_value('user', 'name', '')
            config['user.email'] = cw.get_value('user', 'email', '')
            config['core.autocrlf'] = cw.get_value('core', 'autocrlf', False)

        return config
    


    def valid_global_config(self) -> bool:
        config = self.get_global_config()
        return (
            config['user.name']
            and config['user.email']
        )



    def set_global_config(self, config : dict) -> bool:
        with GitConfigParser(os.path.expanduser('~/.gitconfig'), read_only=False) as cw:
            try:
                cw.set_value('user', 'name', config['user.name'])
                cw.set_value('user', 'email', config['user.email'])
                cw.set_value('core', 'autocrlf', config['core.autocrlf'])
                return True
            except KeyError:
                self.logger.exception('Failed to save global Git configuration:')
                return False