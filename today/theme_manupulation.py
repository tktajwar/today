import json
import os
from shutil import copyfile

from . import paths
from . import settings_manupulation

# get settings data
settings = settings_manupulation.settings

def load():
    '''
    load theme
    '''

    update()
    with open(os.path.join(paths.themes_path, settings['theme'] + '.json'), 'r') as data:
            theme = json.load(data)
    return(theme)

def update():
    '''
    add themes from source that are not in themes directory
    '''

    # list of all the themes directory
    themes_ls = os.listdir(paths.themes_path)

    # for each theme not in themes directory, copy it there
    for theme in os.listdir(paths.themes_source):
        if(theme not in themes_ls):
            copyfile(os.path.join(paths.themes_source, theme), os.path.join(paths.themes_path, theme))
            print(f"Copied theme {theme} to {paths.themes_path}")
