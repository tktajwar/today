import json
from os.path import join
from os import listdir, remove

from . import paths

tasks = {}

def newday():
    '''
    start a new task data
    '''

    global tasks

    # save task data as yesterday's
    with open(paths.yesterday_path, 'w') as data:
        json.dump(tasks, data)

    # make blank task data and save
    tasks = []
    write()

def purge():
    '''
    purge task data
    '''

    global tasks

    # sade task data as purged
    with open(paths.purged_path, 'w') as data:
        json.dump(tasks, data)

    # make blank task data and save
    tasks = []
    write()

def retrieve():
    '''
    retrieve purged data
    '''

    global tasks

    # open purged data and save as current task data
    try:
        with open(paths.purged_path, 'r') as data:
            tasks = json.load(data)
            write()

    except FileNotFoundError:
        print("Therer is no Purged Data file. Purged Data file is only generated when purge function is called.")

def write():
    '''
    write task dat
    '''

    with open(paths.data_path, 'w') as data:
        json.dump(tasks, data)

def read():
    '''
    read task data
    '''

    global tasks
    try:
        with open(paths.data_path, 'r') as data:
            tasks = json.load(data)
    except FileNotFoundError:
        print('Data file does not exist. Creating a new one.')
        tasks = []
        write()

def save(filename='default'):
    '''
    save task data in a file
    '''

    filename = filename + '.json'
    with open(join(paths.save_path, filename), 'w') as data:
        json.dump(tasks, data)

def load(filename='default'):
    '''
    load task data from a file
    '''

    filename = filename + '.json'
    global tasks
    try:
        with open(join(paths.save_path, filename), 'r') as data:
            save(filename='_') # backup current task data
            tasks = json.load(data)
            write()
    except FileNotFoundError:
        print(f"No file saved with the name {filename}.")

def delete(filename='default', every=False):
    '''
    delete a task file
    '''

    # delete everything
    if(every):
        for filename in listdir(paths.save_path):
            if(filename.endswith('.json')):
                file = join(paths.save_path, filename)
                remove(file)

    filename = filename + '.json'
    try:
        remove(join(paths.save_path, filename))
    except FileNotFoundError:
        print(f"No file saved with the name {filename}.")

def list():
    '''
    list all the task files
    '''

    for file in listdir(paths.save_path):
        if(file.endswith('.json')):
            print(file[:-5])

# read task data
read()
