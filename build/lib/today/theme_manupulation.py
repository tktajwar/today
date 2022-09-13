import json
import os
from shutil import copyfile

from . import paths
from . import settings_manupulation

settings = settings_manupulation.settings

def load():
    update()
    with open(os.path.join(paths.themes_path, settings['theme'] + '.json'), 'r') as data:
            theme = json.load(data)
    return(theme)

def update():
    themes_ls = os.listdir(paths.themes_path)
    for theme in os.listdir(paths.themes_source):
        if(theme not in themes_ls):
            copyfile(os.path.join(paths.themes_source, theme), os.path.join(paths.themes_path, theme))
            print(f"Copied theme {theme} to {paths.themes_path}")


def create():
    name = 'matrix'
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

    path = 'themes/' + name + '.json'
    with open(path, 'w') as data:
        json.dump(theme, data)
