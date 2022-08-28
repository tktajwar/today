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
        "duration": int(duration),
        "done": False,
        "priority": priority
        }
    
    tasks.append(task)

def display():
    time = time_start
    for n in ['ID', 'Time', 'Name', 'Duration', 'Done']:
        print(n, end='\t')
    print()
    for i in range(len(tasks)):
        print(i, end='\t')
        print(time, end='\t')
        for attr in tasks[i]:
            print(tasks[i][attr], end='\t')
#        print(f"{i}{' '*(lengths['id'] - len(str(i)))}", end=' ')
#        print(f"{time}{''*(lengths['time']-len(str(time)))}", end=' ')
#        print(f"{t[i]['name']}{' '*(lengths['name'] - len(tO

        print() ; time += tasks[i]['duration']
#    for t in tasks:
#        print(time, t['name'], t['duration'], t['done'])
#        time += t['duration']

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

def write_json():
    with open('data.json', 'w') as data:
        json.dump(tasks, data)

def read_json():
    global tasks
    with open('data.json', 'r') as data:
        tasks = json.load(data)

# main
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

