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
    time = settings['time_start']

    def print_header(name):
        print(f'\033[4m\033[95m{n:8}\033[0m', end=' ')

    def print_attr(attr):
        print(f"{str(attr):8}", end=' ')

    for n in ['ID', 'Time', 'Name', 'Duration', 'Skip', 'Done']:
        print_header(n)
    print()

    for i in range(len(tasks)):
        print_attr(i)
        print_attr(time)
        for key in tasks[i]:
            print_attr(tasks[i][key])
        print() ; time += tasks[i]['duration']

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
parser.add_argument('--done', dest='accumulate', action='store_const', const=task_do, default=display, help='Mark a task as done')
args = parser.parse_args()
print(args.accumulate(args.integers))
