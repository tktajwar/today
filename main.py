# import
import json
import sys

# variables
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

def display():
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
read_settings()
read_json()

if(len(sys.argv)>1):
    if(sys.argv[1]=='add'):
            if(sys.argv[2] and sys.argv[3]):
                create_task(sys.argv[2], sys.argv[3])
                write_json()
    elif(sys.argv[1]=='purge'):
        purge()
    else:
        print(f'Unknown Command: {sys.argv[1]}')
else:
    display()

