import json
import os

import paths
import theme_manupulation
import theme_manupulation

default_settings = {
        'time_start': 420,
        'theme': 'sunrise',
        'default': {
            'name': 'Unnamed',
            'duration': 30
            }
        }

settings = {}

def write():
    with open(paths.settings_path, 'w') as data:
        json.dump(settings, data) 

def read():
    global settings
    try:
        with open(paths.settings_path, 'r') as data:
            settings = json.load(data)
            update()
    except FileNotFoundError:
        print('Settings file does not exist. Creating a new one.')
        settings = default_settings
        write()

def update():
    global settings
    for key, value in default_settings.items():
        updated = []
        if(not(key in settings)):
            settings[key] = value
            updated.append(key)
        if(updated):
            write()
            print(f"Settings were updated, new key(s) added: {updated}")

def change():
    global settings
    theme = theme_manupulation.load()

    def change_key(key, h, d=settings):
        print(f"{theme['highlight']['id']}{key} {theme['escape']}({type(key)})")
        print(h)
        new_value = input(f"Current: {d[key]}, New: ")
        if(new_value):
            new_value = type(d[key])(new_value)
            d[key] = new_value

    print(f"{theme['highlight']['header']}today settings configurator{theme['escape']}")
    print("Write the new settings value for each key and press Enter; leave Blank and press Enter to keep the old value")

    change_key('time_start', "When does your day start? By Default, it's 7 in the morning.")
    change_key('theme', "theme name")
    print(f"{theme['highlight']['undone']}Default Task Values{theme['escape']}: the values today uses if user has not provided the argument when creating a new task")
    change_key('name', "default task name", d=settings['default'])
    change_key('duration', "default task duration", d=settings['default'])
    write()

def change_theme():
    global settings
    theme = theme_manupulation.load()

    def theme_name(t):
        return(t[:-5])

    print(f"Current theme: {settings['theme']}")
    print(f"{theme['highlight']['header']}Available Themes:{theme['escape']}")
    themes_ls = os.listdir(paths.themes_path)
    themes_ls = list(map(theme_name, themes_ls))
    for i, t in enumerate(themes_ls):
        print(f"{theme['highlight']['id']}{i}{theme['escape']}\t{t}")
    try:
        ui = int(input("Select theme: "))
        settings['theme'] = themes_ls[ui]
        write()
    except ValueError:
        print("Select using the ID number.")
    except IndexError:
        print("Invalid ID!")

paths.check_and_create()
read()
