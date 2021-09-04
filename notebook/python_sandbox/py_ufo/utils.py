import os
import pathlib

def get_repos_root():
    return os.path.join(pathlib.Path.home(), r'repos')

def get_web_root():
    return os.path.join(get_repos_root(), 'anylox.git.io')

def get_fortyfive_root():
    return os.path.join(get_repos_root(), 'fortyfive')