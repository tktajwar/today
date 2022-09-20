import json

from . import theme_manupulation
from . import data_manupulation
from . import paths
from . import settings_manupulation
from . import time_formatting

# get settings data
settings = settings_manupulation.settings

# get tasks data
tasks = data_manupulation.tasks

# create a new task
def create(id=None, name=None, duration=None, skip=False, done=False, start_at=None):
    global tasks
    
    # use default values if arguments are not provided
    if(not(name)):
        name = settings['default']['name']

    if(not(duration)):
        duration = settings['default']['duration']

    # create task
    task = {
        "name": name,
        "duration": int(duration),
        'skip': skip,
        "done": done,
        }

    # find the appropriate id if start time is provided
    if(type(start_at)==int):
        task['start_at'] = start_at
        tasks.insert(get_next(start_at), task)

    # else, use the id if provided
    elif(type(id)==int):
        tasks.insert(id, task)

    # else, append
    else:
        tasks.append(task)

    # write task data
    data_manupulation.write()
    return(True)

# remove task
def task_remove(id=None):
    global tasks

    # if ID is provided then remove that task
    if(type(id)==int):
        tasks.pop(id)

    # else, remove the last task
    else:
        tasks.pop()

    # write task data
    data_manupulation.write()

# modify task
def task_modify(id=None, new_id=None, name=None, duration=None, start_at=None):
    global tasks

    # if no ID is passed then pick the last task
    if(type(id) != int):
        id=len(tasks)-1

    # modify name
    if(name):
        tasks[id]['name'] = name

    # modify duration
    if(duration):
        tasks[id]['duration'] = duration

    # modify task start time
    if(type(start_at)==int):
        # remove start time
        if(start_at == -1):
            tasks[id].pop('start_at', None)

        # change start time
        else:
            new_id = get_next(start_at) # get the new ID now that start time is changed
            tasks[id]['start_at'] = start_at

    # modify ID
    if(type(new_id)==int):
        task = tasks[id]
        tasks.pop(id)
        tasks.insert(new_id, task)
    data_manupulation.write()

# display tasks
def display(tasks, id=None):
    # load theme
    theme = theme_manupulation.load()

    # if ID is provided, print that task
    if(type(id)==int):
        if(id<len(tasks)):
            print(tasks[id])
            return(True)
        else:
            raise ValueError(f"No Task with the {theme['highlight']['id']}ID {id}{theme['escape']} exists.")

    # time passed's initial value is the time user set for when their day start
    time = settings['time_start']

    # get max lenghts of each attributes for padding
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

    # header printing functino
    def print_header(name, l):
        print(theme['highlight']['header'], end='')
        print(f"{name:{l}}", end='')
        print(theme['escape'], end=' ')

    # attribute printing function
    def print_attr(attr, l):
        print(f"{str(attr):{l}}", end=' ')

    # print headers
    for attr, i in zip(['ID', 'Time', 'Name', 'Duration', 'Skip', 'Done'], lengths):
        print_header(attr, i)
    print()

    # new task that is neither done nor marked to skip
    next_undone = get_first({'done':False, 'skip': False})

    # for code reuse
    keys = ['skip', 'done']

    for i in range(len(tasks)):
        # if task has start time
        if('start_at' in tasks[i]):
            if(type(tasks[i]['start_at'])==int):
                time = tasks[i]['start_at']

        # print highlighting
        if(tasks[i]['done']): # done task
            print(theme['highlight']['done'], end='')
        elif(tasks[i]['skip']): # skipped task
            print(theme['highlight']['skip'], end='')
        else:
            if(i == next_undone): # next task to do
                print(theme['highlight']['next']['col'], end='')
            else: # undone task
                if(i%2==0):
                    print(theme['highlight']['undone']['even'], end='')
                else:
                    print(theme['highlight']['undone']['odd'], end='')

        # print ID
        print_attr(i, lengths[0])

        # print time
        print_attr(time_formatting.to_time(time), lengths[1])

        # print name
        print_attr(tasks[i]['name'], lengths[2])

        # print duration
        print_attr(time_formatting.to_time(tasks[i]['duration']), lengths[3])

        # print other attributes
        for j, key in enumerate(keys):
            value = tasks[i][key]
            print_attr(value, lengths[j+4])

        # increase time
        time += tasks[i]['duration']

        if(i == next_undone and theme['highlight']['next']['pointer']):
            print(theme['highlight']['next']['pointer'], end='') # print pointer
        print(theme['escape'])

    # the time last task ends
    print(f"{theme['highlight']['skip']}-> {time_formatting.to_time(time)}{theme['escape']}") 
    return(True)

# display today
def display_today(id=None):
    display(tasks=tasks, id=id)

# display yesterday
def display_yesterday(id=None):
    try:
        with open(paths.yesterday_path, 'r') as data:
            yesterday = json.load(data)
            display(tasks=yesterday, id=id)

    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")



# mark a task as done
def task_do(id):
    # get first undone task if ID is not provided
    if(type(id) != int):
        id = get_first({'done': False, 'skip':False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    # if task is already done
    if(tasks[id]['done']):
        print(f"Task {id}: {tasks[id]['name']} was already done.")

    # else, mark task as done
    else:
        tasks[id]['done'] = True
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m done.")

        # write data
        data_manupulation.write()

# mark a task as undone
def task_undo(id=None):
    # get first done task if ID is not provided
    if(type(id) != int):
        id = get_first({'done': True, 'skip':False}, -1)
        if(type(id) != int):
            print("All Tasks are already undone")
            return(False)

    # if task is already marked undone
    if(not(tasks[id]['done'])):
        print(f"Task {id}: {tasks[id]['name']} was not marked done.")

    # else, mark undone the task
    else:
        tasks[id]['done'] = False
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m is marked undone.")

        # write data
        data_manupulation.write()

# mark all tasks as done
def task_do_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = True

    # write data
    data_manupulation.write()

# mark all tasks as undone
def task_undo_all():
    for id in range(len(tasks)):
        tasks[id]['done'] = False

    # write data
    data_manupulation.write()

# toggle skip of a task
def task_toggle_skip(id=None):
    # get the first undone task if no ID was provided
    if(type(id) != int):
        id = get_first({'done': False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    # toggle skip of task
    tasks[id]['skip'] = not tasks[id]['skip']

    # write data
    data_manupulation.write()

# get first task that matches given key:value
def get_first(d: dict, step=1):
    def check(i, key):
        return(tasks[i][key] == d[key])
    for i in range(len(tasks))[::step]:
        matches = [check(i, key) for key in d]
        if(all(matches)):
            return(i)
    return(False)
 
# get the ID where a task will fit based on it's time
def get_next(given_time):
    # time when the day starts
    time = settings['time_start']

    # get to the point when time is larger than given time, return that ID
    for i, task in enumerate(tasks):
        if 'start_at' in task:
            time = task['start_at']

        time += task['duration']

        if(time > given_time):
            return(i)

    # if we never reach that point, return length
    return(len(tasks))
