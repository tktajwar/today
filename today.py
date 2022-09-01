#!/usr/bin/python3
# import
import json
import argparse

# variables and parsing arguments
parser = argparse.ArgumentParser('plan and execute your day in an organised way')
tasks = []
settings = {}

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
    if(id):
        tasks.insert(id, task)
    else:
        tasks.append(task)
    write_json()

def task_remove(id=None):
    global tasks
    if(id or id==0):
        tasks.pop(id)
    else:
        tasks.pop()
    write_json()


def display(id=None, tasks=tasks):
    if(id):
        if(id<len(tasks)):
            print(tasks[id])
            return(True)
        else:
            raise ValueError(f"No Task with the \033[91mID {id}\33[0m exists.")

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
        print(f'\033[4m\033[95m{name:{l}}\033[0m', end=' ')

    def print_attr(attr, l):
        print(f"{str(attr):{l}}", end=' ')

    for attr, i in zip(['ID', 'Time', 'Name', 'Duration', 'Skip', 'Done'], lengths):
        print_header(attr, i)
    print()

    next_undone = get_first({'done':False, 'skip': False})
    for i in range(len(tasks)):
        if(tasks[i]['done']):
            print('\033[32m', end='')
        elif(tasks[i]['skip']):
            print('\033[90m', end='')
        else:
            print('\033[93m', end='')
            if(i == next_undone):
                print('\33[100m', end='')

        print_attr(i, lengths[0])
        print_attr(to_time(time), lengths[1])
        for key, j in zip(tasks[i], range(len(tasks[i]))):
            value = tasks[i][key]
            if(key=='duration'):
                value = to_time(value)
            print_attr(value, lengths[j+2])
        time += tasks[i]['duration']
        print('\033[0m')
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
    with open('yesterday.json', 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write_json()

def display_yesterday(id=None):
    try:
        with open('yesterday.json', 'r') as data:
            yesterday = json.load(data)
            display(id=id, tasks=yesterday)
    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")

def purge():
    global tasks
    with open('purged.json', 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write_json()

def retrieve():
    global tasks
    try:
        with open('purged.json', 'r') as data:
            tasks = json.load(data)
            write_json()
    except FileNotFoundError:
        print("Therer is no Purged Data file. Purged Data file is only generated when purge function is called.")

def write_json():
    with open(settings['data_path'], 'w') as data:
        json.dump(tasks, data)

def read_json():
    global tasks
    try:
        with open(settings['data_path'], 'r') as data:
            tasks = json.load(data)
    except FileNotFoundError:
        print('Data file does not exist. Creating a new one.')
        tasks = []
        write_json()

## settings functions
def write_settings():
    with open('settings.json', 'w') as data:
        json.dump(settings, data) 

def read_settings():
    global settings
    try:
        with open('settings.json', 'r') as data:
            settings = json.load(data)
    except FileNotFoundError:
        print('Settings file does not exist. Creating a new one.')
        settings = {
                'time_start': 420,
                'data_path': 'data.json',
                'default': {
                    'name': 'Unnamed',
                    'duration': 30
                    }
                }
        write_settings()

## formation functins
def to_time(m):
    t = str(m//60)
    t = f"{t}:{str(m%60):0<2}"
    return(t)

# main
## read files
read_settings()
read_json()

## parse user arguments
### positional arguments
parser.add_argument('arguments', metavar='Arguments', nargs='*', help='Task ID [int], Name [str], Duration (minutes) [int]')
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
###
args = parser.parse_args()

a_id, a_name, a_duration = None, None, None
if(args.arguments):
    if(len(args.arguments) == 1): # if only one argument is passed then it's either ID or Name
        if(args.arguments[0].isnumeric()):
            a_id = int(args.arguments[0])
        else:
            a_name = args.arguments[0]
    elif(args.arguments[0].isnumeric()): # ID + Name and/or Duration
        a_id = int(args.arguments[0])
        if(args.arguments[-1].isnumeric()):
            a_duration = int(args.arguments[-1])
            if(len(args.arguments)>2): # everything in the middle is Name
                a_name = " ".join(args.arguments[1:-1])
        else: # everything to the end is Name
            a_name = " ".join(args.arguments[1:])
    else: # Name + Duration(*)
        if(args.arguments[-1].isnumeric()): # Name + Duration
            a_duration = int(args.arguments[-1])
            a_name = " ".join(args.arguments[:-1])
        else: # Name only
            a_name = " ".join(args.arguments)

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
else:
    display_today(a_id)
