#!/usr/bin/env python3
# import
import json
import argparse
import os
import re
from shutil import copyfile

# variables and parsing arguments
## parser
parser = argparse.ArgumentParser('plan and execute your day in an organised way')
##
tasks = []
settings = {}
default_settings = {
        'time_start': 420,
        'theme': 'sunrise',
        'default': {
            'name': 'Unnamed',
            'duration': 30
            }
        }
## paths
path = os.path.expanduser('~')
path = os.path.join(path, '.today')
data_path = os.path.join(path, "data.json")
settings_path = os.path.join(path, "settings.json")
purged_path = os.path.join(path, "purged.json")
yesterday_path = os.path.join(path, "yesterday.json")
themes_path = os.path.join(path, 'themes')
notes_path = os.path.join(path, 'notes.json')

dir_path = os.path.dirname(__file__)
themes_source = os.path.join(dir_path, 'themes')

# functions
## task manipulation functions
def create_task(id=None, name=None, duration=None, skip=False, done=False):
    global tasks

    if(not(name)):
        name = settings['default']['name']
    if(not(duration)):
        duration = settings['default']['duration']

    task = {
        "name": name,
        "duration": int(duration),
        'skip': skip,
        "done": done,
        }
    if(type(id)==int):
        tasks.insert(id, task)
    else:
        tasks.append(task)
    write_json()

def task_remove(id=None):
    global tasks
    if(type(id)==int):
        tasks.pop(id)
    else:
        tasks.pop()
    write_json()


def display(tasks, id=None):
    theme = load_theme()
    if(type(id)==int):
        if(id<len(tasks)):
            print(tasks[id])
            return(True)
        else:
            raise ValueError(f"No Task with the {theme['highlight']['id']}ID {id}{theme['escape']} exists.")

    time = settings['time_start']

    def get_attr_lengths():
        lengths = []
        lengths.append(max(len(str(len(tasks))), 2))
        lengths.append(max(len(to_time(sum(tasks[i]['duration'] for i in range(len(tasks)))+time)), 4))
        for attr in ['name', 'duration', 'skip', 'done']:
            length = 8
            if(len(tasks)):
                length = max(max(len(str(tasks[i][attr])) for i in range(len(tasks))), 8)
            lengths.append(length)
        return(lengths)
    lengths = get_attr_lengths()

    def print_header(name, l):
        print(theme['highlight']['header'], end='')
        print(f"{name:{l}}", end='')
        print(theme['escape'], end=' ')

    def print_attr(attr, l):
        print(f"{str(attr):{l}}", end=' ')

    for attr, i in zip(['ID', 'Time', 'Name', 'Duration', 'Skip', 'Done'], lengths):
        print_header(attr, i)
    print()

    next_undone = get_first({'done':False, 'skip': False})
    for i in range(len(tasks)):
        if(tasks[i]['done']):
            print(theme['highlight']['done'], end='')
        elif(tasks[i]['skip']):
            print(theme['highlight']['skip'], end='')
        else:
            if(i == next_undone):
                print(theme['highlight']['next']['col'], end='')
            else:
                if(i%2==0):
                    print(theme['highlight']['undone']['even'], end='')
                else:
                    print(theme['highlight']['undone']['odd'], end='')

        print_attr(i, lengths[0])
        print_attr(to_time(time), lengths[1])
        for key, j in zip(tasks[i], range(len(tasks[i]))):
            value = tasks[i][key]
            if(key=='duration'):
                value = to_time(value)
            print_attr(value, lengths[j+2])
        time += tasks[i]['duration']
        if(i == next_undone and theme['highlight']['next']['pointer']):
            print(theme['highlight']['next']['pointer'], end='')
        print(theme['escape'])
    return(True)

def display_today(id=None):
    display(tasks=tasks, id=id)

def task_do(id):
    if(type(id) != int):
        id = get_first({'done': False, 'skip':False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    if(id>=len(tasks)):
        raise ValueError(f"No Task with the \033[91mID {id}\33[0m exists.")
    if(tasks[id]['done']):
        print(f"Task {id}: {tasks[id]['name']} was already done.")
    else:
        tasks[id]['done'] = True
        write_json()
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m done.")

def task_undo(id=None):
    if(type(id) != int):
        id = get_first({'done': True, 'skip':False}, -1)
        if(type(id) != int):
            print("All Tasks are already undone")
            return(False)

    if(id>=len(tasks)):
        raise ValueError(f"No Task with the ID {id} exists.")
    if(not(tasks[id]['done'])):
        print(f"Task {id}: {tasks[id]['name']} was not marked done.")
    else:
        tasks[id]['done'] = False
        write_json()
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m is marked undone.")

def task_do_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = True
    write_json()

def task_undo_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = False
    write_json()

def task_toggle_skip(id=None):
    if(type(id) != int):
        id = get_first({'done': False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    if(id>=len(tasks)):
        raise ValueError(f"No Task with the \033[91mID {id}\33[0m exists.")
    tasks[id]['skip'] = not tasks[id]['skip']
    write_json()

## Task Tool Functions
def get_first(d: dict, step=1):
    def check(i, key):
        return(tasks[i][key] == d[key])
    for i in range(len(tasks))[::step]:
        matches = [check(i, key) for key in d]
        if(all(matches)):
            return(i)
    return(False)
    
## data manipulation functions
def newday():
    global tasks
    with open(yesterday_path, 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write_json()

def display_yesterday(id=None):
    try:
        with open(yesterday_path, 'r') as data:
            yesterday = json.load(data)
            display(tasks=yesterday, id=id)
    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")

def purge():
    global tasks
    with open(purged_path, 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write_json()

def retrieve():
    global tasks
    try:
        with open(purged_path, 'r') as data:
            tasks = json.load(data)
            write_json()
    except FileNotFoundError:
        print("Therer is no Purged Data file. Purged Data file is only generated when purge function is called.")

def write_json():
    with open(data_path, 'w') as data:
        json.dump(tasks, data)

def read_json():
    global tasks
    try:
        with open(data_path, 'r') as data:
            tasks = json.load(data)
    except FileNotFoundError:
        print('Data file does not exist. Creating a new one.')
        tasks = []
        write_json()

## notes functions
def show_notes(id=None):
    notes = read_notes()
    theme = load_theme()
    if(id):
        print(notes[id])
        return(True)
    for i in range(len(notes)):
        print(f"{theme['highlight']['id']}{i}{theme['escape']}: {notes[i]}")

def write_notes(notes):
    with open(notes_path, 'w') as data:
        json.dump(notes, data)

def read_notes():
    notes=[]
    try:
        with open(notes_path, 'r') as data:
            notes = json.load(data)
    except FileNotFoundError:
        print('Notes file does not exist. Creating a new one.')
        write_notes(notes)
        return(False)
    return(notes)

def add_notes(note, id=None):
    notes = read_notes()
    if(type(id)==int):
        notes.insert(note, id)
    else:
        notes.append(note)
    write_notes(notes)

def remove_notes(id=None):
    notes = read_notes()
    if(type(id)==int):
        notes.pop(note, id)
    else:
        notes.pop(note)
    write_notes(notes)

## settings functions
def write_settings():
    with open(settings_path, 'w') as data:
        json.dump(settings, data) 

def read_settings():
    global settings
    try:
        with open(settings_path, 'r') as data:
            settings = json.load(data)
            update_settings()
    except FileNotFoundError:
        print('Settings file does not exist. Creating a new one.')
        settings = default_settings
        write_settings()

def update_settings():
    global settings
    for key, value in default_settings.items():
        updated = []
        if(not(key in settings)):
            settings[key] = value
            updated.append(key)
        if(updated):
            write_settings()
            print(f"Settings was updated, new key(s) added: {updated}")

def change_settings():
    global settings
    theme = load_theme()

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

    write_settings()

def load_theme():
    get_themes()
    with open(os.path.join(themes_path, settings['theme'] + '.json'), 'r') as data:
            theme = json.load(data)
    return(theme)

def get_themes():
    theme_dir = os.listdir(themes_path)
    for theme in os.listdir(themes_source):
        if(theme not in theme_dir):
            copyfile(os.path.join(themes_source, theme), os.path.join(themes_path, theme))

## formation functins
def to_time(m):
    hour = (m//60)%24
    minute = m%60
    t = f"{hour}:{str(minute):0<2}"
    return(t)

def to_min(duration):
    m = re.match("^(\d+)(\w)$", duration)
    if(not(m)):
        return(None)
    if(m.group(2)=='h'):
        return(int(m.group(1))*60)
    elif(m.group(2)=='d'):
        return(int(m.group(1))*60*24)
    elif(m.group(2)=='s'):
        return(int(m.group(1))/60)
    else:
        return(int(m.group(1)))

def is_duration(s):
    m = re.match("^(\d+)(\w)$", s)
    if(m):
        return(True)
    return(False)

# main
###create root directory if it does not exist
if (not(os.path.exists(path))):
    print(f"creating directory: {path}")
    os.makedirs(path)
if (not(os.path.exists(themes_path))):
    os.makedirs(themes_path)
    get_themes()

# read files
read_settings()
read_json()

## parse user arguments
### positional arguments
parser.add_argument('arguments', metavar='Arguments', nargs='*', help='Task ID [int], Name [str], Duration [int]')
### positional requiring options
parser.add_argument('-a', '--add', action='store_true', help='add/append a new Task [?ID][Name][Duration]')
parser.add_argument('-d', '--done', action='store_true', help='mark a task as done [ID]')
parser.add_argument('-u', '--undo', action='store_true', help='mark a task as undone [ID]')
parser.add_argument('-r', '--remove', action='store_true', help='remove Task [ID]')
parser.add_argument('-t', '--toggle', action='store_true', help='toggle Skip of Task [ID]')
### non positional requiring options
parser.add_argument('-da', '--done-all', action='store_true', help='mark all tasks as done')
parser.add_argument('-ua', '--undo-all', action='store_true', help='mark all tasks as undone')
parser.add_argument('-p', '--purge', action='store_true', help='purge Task Data')
parser.add_argument('-v', '--retrieve', action='store_true', help='retrieve from Purged Task Data')
parser.add_argument('-n', '--new-day', action='store_true', help='store current Task Data as Yesterday and start a new Day')
parser.add_argument('-y', '--yesterday', action='store_true', help='Show Yesterday\'s Data')
parser.add_argument('-c', '--settings', action='store_true', help='configure settings data')
parser.add_argument('-g', '--read-notes', action='store_true', help='show notes')
parser.add_argument('-w', '--add_note', action='store_true', help='add a new note')
parser.add_argument('-x', '--delete_note', action='store_true', help='delete a note')

###
args = parser.parse_args()

a_id, a_name, a_duration = None, None, None
if(args.arguments):
    if(len(args.arguments) == 1): # if only one argument is passed then it's either ID or Name
        if(args.arguments[0].isnumeric()):
            a_id = int(args.arguments[0])
        elif(is_duration(args.arguments[0])):
            a_duration = args.arguments[0]
        else:
            a_name = args.arguments[0]
    elif(args.arguments[0].isnumeric()): # ID + Name and/or Duration
        a_id = int(args.arguments[0])
        if(args.arguments[-1].isnumeric() or is_duration(args.arguments[-1])):
            a_duration = args.arguments[-1]
            if(len(args.arguments)>2): # everything in the middle is Name
                a_name = " ".join(args.arguments[1:-1])
        else: # everything to the end is Name
            a_name = " ".join(args.arguments[1:])
    else: # Name + Duration(*)
        if(args.arguments[-1].isnumeric() or is_duration(args.arguments[-1])): # Name + Duration
            a_duration = args.arguments[-1]
            a_name = " ".join(args.arguments[:-1])
        else: # Name only
            a_name = " ".join(args.arguments)
if(a_duration):
    if(is_duration(a_duration)):
        a_duration = to_min(a_duration)
    else:
        a_duration = int(a_duration)

if(args.add):
    create_task(a_id, a_name, a_duration)
elif(args.done):
    task_do(a_id)
elif(args.undo):
    task_undo(a_id)
elif(args.remove):
    task_remove(a_id)
elif(args.toggle):
    task_toggle_skip(a_id)
elif(args.done_all):
    task_do_all()
elif(args.undo_all):
    task_undo_all()
elif(args.purge):
    purge()
elif(args.retrieve):
    retrieve()
elif(args.new_day):
    newday()
elif(args.yesterday):
    display_yesterday(a_id)
elif(args.settings):
    change_settings()
elif(args.read_notes):
    show_notes(a_id)
elif(args.add_note):
    add_notes(a_name, a_id)
elif(args.remove_note):
    remove_note(a_id)
else:
    display_today(a_id)
