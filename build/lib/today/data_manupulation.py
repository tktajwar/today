import json

from . import paths

tasks = {}

def newday():
    global tasks
    with open(paths.yesterday_path, 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write()

def display_yesterday(id=None):
    try:
        with open(paths.yesterday_path, 'r') as data:
            yesterday = json.load(data)
            display(tasks=yesterday, id=id)
    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")

def purge():
    global tasks
    with open(paths.purged_path, 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write()

def retrieve():
    global tasks
    try:
        with open(paths.purged_path, 'r') as data:
            tasks = json.load(data)
            write()
    except FileNotFoundError:
        print("Therer is no Purged Data file. Purged Data file is only generated when purge function is called.")

def write():
    with open(paths.data_path, 'w') as data:
        json.dump(tasks, data)

def read():
    global tasks
    try:
        with open(paths.data_path, 'r') as data:
            tasks = json.load(data)
    except FileNotFoundError:
        print('Data file does not exist. Creating a new one.')
        tasks = []
        write()

read()
