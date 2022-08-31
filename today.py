# import
import json
import argparse

# variables and parsing arguments
parser = argparse.ArgumentParser('Process Task Arguments')
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
            raise ValueError(f"No Task with the ID {id} exists.")
        


    time = settings['time_start']

    def get_attr_lengths():
        lengths = []
        lengths.append(max(len(str(len(tasks))), 4))
        lengths.append(max(len(to_time(sum(tasks[i]['duration'] for i in range(len(tasks))))), 4))
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

    next_done = False
    for i in range(len(tasks)):
        if(tasks[i]['done']):
            print('\033[32m', end='')
        elif(tasks[i]['skip']):
            print('\033[90m', end='')
        else:
            print('\033[93m', end='')
            if(not(next_done)):
                print('\33[100m', end='')
                next_done = True

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
    if(id>len(tasks)):
        raise ValueError(f"No Task with the ID {id} exists.")
    if(tasks[id]['done']):
        print(f"Task {id}: {tasks[id]['name']} was already done.")
    else:
        tasks[id]['done'] = True
        write_json()
        print(f"Task {id}: {tasks[id]['name']} done.")

def task_undo(id):
    if(id>len(tasks)):
        raise ValueError(f"No Task with the ID {id} exists.")
    if(not(tasks[id]['done'])):
        print(f"Task {id}: {tasks[id]['name']} was not marked done.")
    else:
        tasks[id]['done'] = False
        write_json()
        print(f"Task {id}: {tasks[id]['name']} is marked undone.")

def task_do_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = True
    write_json()

def task_undo_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = False
    write_json()

def task_toggle_skip(id):
    tasks[id]['skip'] = not tasks[id]['skip']
    write_json()
    
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
                'time_start': 0,
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
    t = f"{t}:{str(m%60):2}"
    return(t)

# main
## read files
read_settings()
read_json()

## handle arguments
### positional
parser.add_argument('id', metavar='ID', type=int, nargs='?', help='Task ID number')
parser.add_argument('name', metavar='Name', type=str, nargs='?', help='Task Name')
parser.add_argument('duration', metavar='Duration', type=int, nargs='?', help='Task Duration (Minutes)')
### positional requiring
parser.add_argument('-a', '--add', action='store_true', help='add a new Task')
parser.add_argument('-d', '--done', action='store_true', help='mark a task as done')
parser.add_argument('-u', '--undo', action='store_true', help='mark a task as undone')
parser.add_argument('-r', '--remove', action='store_true', help='remove Task')
parser.add_argument('-t', '--toggle', action='store_true', help='toggle Skip of Task')
### non positional requiring
parser.add_argument('-da', '--done-all', action='store_true', help='mark all tasks as done')
parser.add_argument('-ua', '--undo-all', action='store_true', help='mark all tasks as undone')
parser.add_argument('-p', '--purge', action='store_true', help='purge Task Data')
parser.add_argument('-v', '--retrieve', action='store_true', help='retrieve from Purged Task Data')
parser.add_argument('-n', '--new-day', action='store_true', help='store current Task Data as Yesterday and start a New Day')
parser.add_argument('-y', '--yesterday', action='store_true', help='Show Yesterday\'s Data')
###
args = parser.parse_args()
if(args.add):
    create_task(args.id, args.name, args.duration)
elif(args.done):
    task_do(args.id)
elif(args.undo):
    task_undo(args.id)
elif(args.remove):
    task_remove(args.id)
elif(args.toggle):
    task_toggle_skip(args.id)
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
    display_yesterday()
else:
    display_today()
