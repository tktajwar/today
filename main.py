# import
import json
import sys

# variables
today_dir = ""
time_start = 0
tasks = []

# functions
## task manipulation functions
def create_task(name, duration, priority=None):
    global tasks

    task = {
        "name": name,
        "duration": duration,
        "done": False,
        "priority": priority
        }
    
    tasks.append(task)

def display():
    time = time_start
    for t in tasks:
        print('Time | Name | Duration | Done')
        print(time, t['name'], t['duration'], t['done'])
        time += t['duration']

## data manipulation functions
def purge():
    global tasks
    tasks = []
    write_json()

def write_json():
    with open('data.json', 'w') as data:
        json.dump(tasks, data)

def read_json():
    global tasks
    with open('data.json', 'r') as data:
        tasks = json.load(data)

# main
if(len(sys.argv)>1):
    if(sys.argv[1]=='add'):
            if(sys.argv[2] and sys.argv[3]):
                create_task(sys.argv[2], sys.argv[3])
                write_json()
    elif(sys.argv[1]=='purge'):
        purge()
    else:
        print(f'Unknown Command: {sys.argv[1]}')
read_json()

display()
