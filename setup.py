#!/usr/bin/env python3

import logging
import glob
import platform
import shutil
import subprocess
import os
from os.path import expanduser

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')
user_home = expanduser("~")
work = False


def check_app(app):
    logger.info(f'Checking for {app}')
    result = subprocess.run(['which', app])
    if result.returncode == 0:
        return True
    else:
        return False


def bash():
    if check_app('bash'):
        logger.info("Setting up Bash")
        shutil.copyfile("bash/.bash_profile", f'{user_home}/.bash_profile')
        shutil.copyfile("bash/.bashrc", f'{user_home}/.bashrc')


def setup(program_list):
    if 'bash' in program_list:
        bash()
    if 'my_programs' in program_list:
        scripts()
    if 'tmux' in program_list:
        tmux()
    if 'vim' in program_list:
        vim()
    if 'zsh' in program_list:
        zsh()


def scripts():
    logger.info("Setting up my scripts")
    subprocess.run(['mkdir', '-p', f'{user_home}/bin'])
    shutil.copy2("scripts/ruby-setup.sh", f'{user_home}/bin/ruby_setup')


def tmux():
    if check_app('tmux'):
        logger.info("Setting up Tmux")
        shutil.copyfile("tmux/.tmux.conf", f'{user_home}/.tmux.conf')


def vim():
    if check_app('vim'):
        logger.info("Setting up Vim")

        if not os.path.exists(f'{user_home}/.vim/bundle/Vundle.vim'):
            subprocess.run(["git","clone", "https://github.com/VundleVim/Vundle.vim.git", f'{user_home}/.vim/bundle/Vundle.vim'])
        subprocess.run(["mkdir", "-p", f'{user_home}/.vim/colors'])
        subprocess.run(["vim", "+PluginInstall", "+qall"])

        for file in glob.glob(f'{user_home}/.vim/bundle/vim-colorschemes/colors/*'):
            shutil.copy(file, f'{user_home}/.vim/colors')

        for file in glob.glob(f'{user_home}/.vim/bundle/vim-railscasts-theme/colors/*'):
            shutil.copy(file, f'{user_home}/.vim/colors')

        shutil.copyfile("vim/.vimrc", f'{user_home}/.vimrc')


def zsh():
    if check_app('zsh'):
        logger.info("Setting up Zsh")
        shutil.copyfile("zsh/.zshrc", f'{user_home}/.zshrc')
        if work:
            with open(f'{user_home}/.zshrc', "a") as myfile:
                myfile.write(f'source "{user_home}/.zshrc-work"')
        shutil.copyfile("zsh/.zshrc-custom", f'{user_home}/.zshrc-custom')
        shutil.copyfile("zsh/greg-kman.zsh-theme", f'{user_home}/.oh-my-zsh/themes/greg-kman.zsh-theme')


def yes_or_no():
    reply = str(input('Work machine (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no()


def main():
    work = yes_or_no()
    if platform.system() == "Darwin":
        logger.info("Mac OSx found")
        setup(['bash', 'my_programs', 'tmux', 'vim', 'zsh'])

    elif platform.system() == "Linux":
        logger.info("Linux found")
        setup(['bash', 'my_programs', 'tmux', 'vim', 'zsh'])

    elif platform.system() == "MINGW64":
        logger.info("Windows Bash found")
        setup(['vim'])

    elif platform.system() == "CYGWIN_NT":
        logger.info("Windows Cygwin found")
        setup(['bash', 'vim', 'zsh'])

    else:
        logger.info("OS is not supported")

if __name__ == "__main__":
    main()
