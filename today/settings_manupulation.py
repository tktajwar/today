import json
import os

from . import paths
from . import theme_manupulation
from . import theme_manupulation
from . import time_formatting

# the settings today will use if settings file does not exist or has missing attributes
default_settings = {
        'time_start': 420, # 7:00
        'theme': 'sunrise',
        'default': {
            'name': 'Unnamed',
            'duration': 30
            }
        }

# settings file
settings = {}

def write():
    '''
    write settings data
    '''

    with open(paths.settings_path, 'w') as data:
        json.dump(settings, data) 

def read():
    '''
    read settings data
    '''

    global settings

    # read settings file
    try:
        with open(paths.settings_path, 'r') as data:
            settings = json.load(data)
            update()

    # use default settings if settings file does not exist
    except FileNotFoundError:
        print('Settings file does not exist. Creating a new one.')
        settings = default_settings
        write()

def update():
    '''
    updates settings (add attributes that is unavailable in currents settings)
    '''

    global settings

    # check if each items in default settings exists in settings and add missing items
    for key, value in default_settings.items():
        updated = []

        if(not(key in settings)):
            settings[key] = value
            updated.append(key)

        if(updated):
            write()
            print(f"Settings were updated, new key(s) added: {updated}")

def change():
    '''
    change settings data
    '''

    global settings
    theme = theme_manupulation.load()

    def change_key(key, h, d=settings, func=None):
        '''
    # function for each keys to change
    '''

        # highlight name of the key
        print(f"{theme['highlight']['id']}{key}{theme['escape']}")

        # print help message
        print(h)

        # user input for new value
        new_value = input(f"Current: {d[key]}, New: ")

        # run a passed function
        if(func):
            new_value=func(new_value)

        # set new value
        if(new_value or type(new_value)==int): # user input != blank
            new_value = type(d[key])(new_value) # make data type of new value same as the old one
            d[key] = new_value

    print(f"{theme['highlight']['header']}today settings configurator{theme['escape']}")
    print("Write the new settings value for each key and press Enter; leave Blank and press Enter to keep the old value")

    # time start
    change_key('time_start', "When does your day start? By Default, it's 7 in the morning.", func=time_formatting.to_min)

    # default task data
    print(f"{theme['highlight']['undone']['even']}Default Task Values{theme['escape']}: the values today uses if user has not provided the argument when creating a new task")
    change_key('name', "default task name", d=settings['default'])
    change_key('duration', "default task duration", d=settings['default'])

    # write settings
    write()

def change_theme():
    '''
    change theme
    '''

    global settings

    # load theme
    theme = theme_manupulation.load()

    def theme_name(t):
        '''
    # theme name -= '.json'
    '''

        return(t[:-5])

    # show help
    print(f"Current theme: {settings['theme']}")
    print(f"{theme['highlight']['header']}Available Themes:{theme['escape']}")
    themes_ls = os.listdir(paths.themes_path)
    themes_ls = list(map(theme_name, themes_ls))
    for i, t in enumerate(themes_ls):
        print(f"{theme['highlight']['id']}{i}{theme['escape']}\t{t}")

    # user select new theme
    try:
        ui = int(input("Select theme: "))
        settings['theme'] = themes_ls[ui]

        # write settings
        write()

    except ValueError:
        print("Select using the ID number.")

    except IndexError:
        print("Invalid ID!")

def change_time(time):
    global settings

    settings['time_start'] = time

    write()

# check and create necessary files and directories
paths.check_and_create()

# read settings
read()
