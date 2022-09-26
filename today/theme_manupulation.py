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

def create():
    '''
    create a new theme
    '''

    # name of theme file
    name = 'matrix'

    # theme
    theme = {
            'highlight': {
                'id': '\33[92m',
                'header': '\33[92m',
                'done': '\33[32m',
                'skip': '\33[30m',
                'undone': {
                    'even': '\33[40m\33[92m',
                    'odd': '\33[40m\33[92m'
                    },
                'next': {
                    'col': '\33[30m\33[102m',
                    'pointer': '\33[5m<---',
                },
            },
            'escape': '\33[0m',
        }

    # save the theme
    path = paths.themes_path + '/' + names + '.json'
    with open(path, 'w') as data:
        json.dump(theme, data)
