# import
import json
import argparse

# variables and parsing arguments
parser = argparse.ArgumentParser('Process Task Arguments')
tasks = []
settings = {}

# functions
## task manipulation functions
def create_task(name, duration,  priority=1, skip=False, done=False):
    global tasks

    task = {
        "name": name,
        "duration": int(duration),
        'skip': skip,
        "done": done,
        }
    
    tasks.append(task)

def display(id=None):
    if(id):
        print(tasks[id])
        return(True)

    time = settings['time_start']

    def get_attr_lengths():
        lengths = []
        lengths.append(max(len(str(len(tasks))), 4))
        lengths.append(max(len(str(sum(tasks[i]['duration'] for i in range(len(tasks))))), 4))
        for attr in ['name', 'duration', 'skip', 'done']:
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
        print_attr(time, lengths[1])
        for key, j in zip(tasks[i], range(len(tasks[i]))):
            value = tasks[i][key]
            print_attr(value, lengths[j+2])
        time += tasks[i]['duration']
        print('\033[0m')
    return(True)

def task_do(id):
    if(id>len(tasks)):
        print('Task ID out of range')
        return(0)
    if(tasks[id]['done']):
        print(f"Task {id}: {tasks[id]['name']} was already done.")
    else:
        tasks[id]['done'] = True
        write_json()
        print(f"Task {id}: {tasks[id]['name']} done.")

## data manipulation functions
def purge():
    global tasks
    with open('purged.json', 'w') as data:
        json.dump(tasks, data)
    tasks = []
    write_json()

def retrieve():
    global tasks
    with opin('purged.json', 'r') as data:
        tasks = json.loads(data)
    write_json()

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
                'data_path': 'data.json'
                }
        write_settings()


# main
## read files
read_settings()
read_json()

## handle arguments
parser.add_argument('integers', metavar='ID', type=int, nargs='?', help='Task ID number')
parser.add_argument('-a', '--add', dest='accumulate', action='store_const', const=task_do, default=display, help='Add a new Task')
parser.add_argument('-d', '--done', dest='accumulate', action='store_const', const=task_do, default=display, help='Mark a task as done')
parser.add_argument('-u', '--undo', dest='accumulate', action='store_const', const=task_do, default=display, help='Mark a task as undone')
parser.add_argument('-t', '--toggle', dest='accumulate', action='store_const', const=task_do, default=display, help='Toggle Skip of Task')
parser.add_argument('-da', '--done-all', dest='accumulate', action='store_const', const=task_do, default=display, help='Mark all tasks as done')
parser.add_argument('-ua', '--undo-all', dest='accumulate', action='store_const', const=task_do, default=display, help='Mark all tasks as undone')
parser.add_argument('-r', '--remove', dest='accumulate', action='store_const', const=task_do, default=display, help='Remove Task')
parser.add_argument('-p', '--purge', dest='accumulate', action='store_const', const=task_do, default=display, help='Purge Task Data')
parser.add_argument('-v', '--retrieve', dest='accumulate', action='store_const', const=task_do, default=display, help='Retrieve from Purged Data')
parser.add_argument('-n', '--newday', dest='accumulate', action='store_const', const=task_do, default=display, help='Store current Task Data as Yesterday and Start a New Day')
parser.add_argument('-y', '--yesterday', dest='accumulate', action='store_const', const=task_do, default=display, help='Show Yesterday\'s Data')
args = parser.parse_args()
args.accumulate(args.integers)
