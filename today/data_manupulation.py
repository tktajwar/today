import json
from os.path import join
from os import listdir, remove

from . import paths

tasks = {}

# start a new task data
def newday():
    global tasks

    # save task data as yesterday's
    with open(paths.yesterday_path, 'w') as data:
        json.dump(tasks, data)

    # make blank task data and save
    tasks = []
    write()

# purge task data
def purge():
    global tasks

    # sade task data as purged
    with open(paths.purged_path, 'w') as data:
        json.dump(tasks, data)

    # make blank task data and save
    tasks = []
    write()

# retrieve purged data
def retrieve():
    global tasks

    # open purged data and save as current task data
    try:
        with open(paths.purged_path, 'r') as data:
            tasks = json.load(data)
            write()

    except FileNotFoundError:
        print("Therer is no Purged Data file. Purged Data file is only generated when purge function is called.")

# write task dat
def write():
    with open(paths.data_path, 'w') as data:
        json.dump(tasks, data)

# read task data
def read():
    global tasks
    try:
        with open(paths.data_path, 'r') as data:
            tasks = json.load(data)
    except FileNotFoundError:
        print('Data file does not exist. Creating a new one.')
        tasks = []
        write()

# save task data in a file
def save(filename='default'):
    filename = filename + '.json'
    with open(join(paths.save_path, filename), 'w') as data:
        json.dump(tasks, data)

# load task data from a file
def load(filename='default'):
    filename = filename + '.json'
    global tasks
    try:
        with open(join(paths.save_path, filename), 'r') as data:
            save(filename='last_unsaved') # save the current task data in a file
            tasks = json.load(data)
            write()
    except FileNotFoundError:
        print(f"No file saved with the name {filename}.")

# delete a task file
def delete(filename='default'):
    filename = filename + '.json'
    try:
        remove(join(paths.save_path, filename))
    except FileNotFoundError:
        print(f"No file saved with the name {filename}.")

# list all the task files
def list():
    for file in listdir(paths.save_path):
        print(file)

# read task data
read()
