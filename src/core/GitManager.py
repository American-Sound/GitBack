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



def is_remote_repository(url) -> str:
    try:
        git_url = Git().execute(['git', 'ls-remote', '--get-url', url])
        return git_url.split('/')[-1].replace('.git', '')
    except GitCommandError:
        return None



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
        self.repo_name = ""
        self.lock = threading.Lock()




    def is_project_checked_out(self) -> bool:
        return self.repo is not None



    def is_dirty(self):
        return self.repo.is_dirty(untracked_files=True)



    def default_branch_checked_out(self):
        return self.repo.active_branch.name in ('main', 'master')



    def get_commission_branches(self) -> list:
        return [head.name for head in self.repo.heads if head.name.startswith('commission-branch')]


    def commission_branch_checked_out(self):
        return self.repo.active_branch.name.startswith('commission-branch-')



    def pull_updates(self):
        self.repo.git.pull()



    def checkout_new_branch(self, branch):
        self.repo.create_head(branch).checkout()




    def checkout_branch(self, branch):
        self.repo.heads[branch].checkout()



    def checkout_default_branch(self):
        if 'origin/main' in [ref.name for ref in self.repo.remote().refs]:
            self.repo.heads['main'].checkout()
        else:
            self.repo.heads['master'].checkout()



    def checkout_local_repo(self, path):
        self.repo = git.Repo(path)
        self.repo_name = os.path.basename(self.repo.working_tree_dir)



    def clone_project(self, url, path):
        self.repo = git.Repo.clone_from(url, path)
        self.repo_name = os.path.basename(self.repo.working_tree_dir)
        self.logger.info(f'Successfully cloned {url} to {path}')



    def add_changes(self):
        self.repo.git.add(['*'])



    def commit_changes(self, message):
        self.repo.git.commit(m=message)



    def push_changes(self):
        self.repo.remote().push(self.repo.active_branch.name)



    def stash(self):
        self.repo.git.stash()



    def stash_pop(self):
        self.repo.git.stash("pop")



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