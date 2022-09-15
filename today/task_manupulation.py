import json

from . import theme_manupulation
from . import data_manupulation
from . import paths
from . import settings_manupulation
from . import time_formatting

settings = settings_manupulation.settings

tasks = data_manupulation.tasks

def create(id=None, name=None, duration=None, skip=False, done=False):
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
    data_manupulation.write()

def task_remove(id=None):
    global tasks
    if(type(id)==int):
        tasks.pop(id)
    else:
        tasks.pop()
    data_manupulation.write()


def display(tasks, id=None):
    theme = theme_manupulation.load()
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
        lengths.append(max(len(time_formatting.to_time(sum(tasks[i]['duration'] for i in range(len(tasks)))+time)), 4))
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
        print_attr(time_formatting.to_time(time), lengths[1])
        for key, j in zip(tasks[i], range(len(tasks[i]))):
            value = tasks[i][key]
            if(key=='duration'):
                value = time_formatting.to_time(value)
            print_attr(value, lengths[j+2])
        time += tasks[i]['duration']
        if(i == next_undone and theme['highlight']['next']['pointer']):
            print(theme['highlight']['next']['pointer'], end='')
        print(theme['escape'])
    print(f"{theme['highlight']['skip']}-> {time_formatting.to_time(time)}{theme['escape']}") # the time last task ends
    return(True)

def display_today(id=None):
    display(tasks=tasks, id=id)

def display_yesterday(id=None):
    try:
        with open(paths.yesterday_path, 'r') as data:
            yesterday = json.load(data)
            display(tasks=yesterday, id=id)
    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")



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
        data_manupulation.write()
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
        data_manupulation.write()
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m is marked undone.")

def task_do_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = True
    data_manupulation.write()

def task_undo_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = False
    data_manupulation.write()

def task_toggle_skip(id=None):
    if(type(id) != int):
        id = get_first({'done': False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    if(id>=len(tasks)):
        raise ValueError(f"No Task with the \033[91mID {id}\33[0m exists.")
    tasks[id]['skip'] = not tasks[id]['skip']
    data_manupulation.write()

## Task Tool Functions
def get_first(d: dict, step=1):
    def check(i, key):
        return(tasks[i][key] == d[key])
    for i in range(len(tasks))[::step]:
        matches = [check(i, key) for key in d]
        if(all(matches)):
            return(i)
    return(False)
 
