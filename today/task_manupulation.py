import json

from . import theme_manupulation
from . import data_manupulation
from . import paths
from . import settings_manupulation
from . import time_formatting
from . import todo

# get settings data
settings = settings_manupulation.settings

# get tasks data
tasks = data_manupulation.tasks

def create(id=None, name=None, duration=None, skip=False, done=False, start_at=None):
    '''
    create a new task
    '''

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

    # insert/append task
    if(type(start_at)==int):
        task['start_at'] = start_at
        tasks.insert(get_next(start_at), task)
    elif(type(id)==int):
        tasks.insert(id, task)
    else:
        tasks.append(task)

    # write task data
    data_manupulation.write()
    return(True)

def task_remove(id=None, every=False):
    '''
    remove task
    '''

    global tasks

    # remove every Tasks
    if(every):
        for _ in range(len(tasks)):
            task_remove(0)
        return(True)

    # remove task
    if(type(id)==int):
        tasks.pop(id)
    else:
        tasks.pop()

    # write task data
    data_manupulation.write()
    
    return(True)

def task_modify(id=None, new_id=None, name=None, duration=None, start_at=None, every=False):
    '''
    modify task
    '''

    global tasks

    # modify every tasks
    if(every):
        for i in range(len(tasks)):
            task_modify(id=i, new_id=new_id, name=name, duration=duration, start_at=start_at, every=False)
        return(True)

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

def display(tasks, id=None):
    '''
    display tasks
    '''

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

    def get_attr_lengths():
        '''
        # get max lenghts of each attributes for padding
        '''

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
        '''
        # header printing functino
        '''

        print(theme['highlight']['header'], end='')
        print(f"{name:{l}}", end='')
        print(theme['escape'], end=' ')

    def print_attr(attr, l):
        '''
        # attribute printing function
        '''

        print(f"{str(attr):{l}}", end=' ')

    # next task
    next_undone = get_first({'done':False, 'skip': False})

    if(not(next_undone)):
        print(f"{theme['highlight']['undone']['even']}All tasks are done.{theme['escape']}")

    # print headers
    for attr, i in zip(['ID', 'Time', 'Name', 'Duration', 'Skip', 'Done'], lengths):
        print_header(attr, i)
    print()

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


    # display todo list
    todo.read()
    if(todo.todo):
        # print headers
        print_header('ID', lengths[0]+lengths[1])
        print_header('Todo', lengths[2])
        print_header('Duration', lengths[3])
        print()

        # print attributes
        for i, task in enumerate(todo.todo):
            print(theme['highlight']['undone']['even'], end='')
            print_attr(i, lengths[0]+lengths[1])
            print_attr(task['name'], lengths[2])
            print_attr(time_formatting.to_time(task['duration']), lengths[3])
            print(theme['escape'])
        return(True)

def display_today(id=None):
    '''
    display today
    '''

    display(tasks=tasks, id=id)

def display_yesterday(id=None):
    '''
    display yesterday
    '''

    try:
        with open(paths.yesterday_path, 'r') as data:
            yesterday = json.load(data)
            display(tasks=yesterday, id=id)

    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")



def task_do(id):
    '''
    mark a task as done
    '''

    # get first undone task if ID is not provided
    if(type(id) != int):
        id = get_first({'done': False, 'skip':False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    # mark task as done
    if(tasks[id]['done']):
        print(f"Task {id}: {tasks[id]['name']} was already done.")
    else:
        tasks[id]['done'] = True
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m done.")

        # write data
        data_manupulation.write()

def task_undo(id=None):
    '''
    mark a task as undone
    '''

    # get first done task if ID is not provided
    if(type(id) != int):
        id = get_first({'done': True, 'skip':False}, -1)
        if(type(id) != int):
            print("All Tasks are already undone")
            return(False)

    # mark task as undone
    if(not(tasks[id]['done'])):
        print(f"Task {id}: {tasks[id]['name']} was not marked done.")
    else:
        tasks[id]['done'] = False
        print(f"\033[91mTask {id}\033[0m: \33[33m{tasks[id]['name']}\033[0m is marked undone.")

        # write data
        data_manupulation.write()

def task_do_all():
    '''
    mark all tasks as done
    '''

    for id in range(len(tasks)):
        tasks[id]['done'] = True

    # write data
    data_manupulation.write()

def task_undo_all():
    '''
    mark all tasks as undone
    '''

    for id in range(len(tasks)):
        tasks[id]['done'] = False

    # write data
    data_manupulation.write()

def task_skip(id=None, every=False):
    '''
    mark skip of a task
    '''
    global tasks

    # skip every Tasks
    if(every):
        for task in tasks:
            task['skip'] = True
        data_manupulation.write()
        return(True)

    # get the next undone task
    if(type(id) != int):
        id = get_first({'done': False, 'skip': False})
        if(type(id) != int):
            print("All Tasks are already done")
            return(False)

    # skip task
    tasks[id]['skip'] = True

    # write data
    data_manupulation.write()

    return(True)
    
def task_unskip(id=None, every=False):
    '''
    unmark skip of a task
    '''
    global tasks

    # unskip every Tasks
    if(every):
        for task in tasks:
            task['skip'] = False 
        data_manupulation.write()
        return(True)

    # get the last skipped task
    if(type(id) != int):
        id = get_first({'skip': True}, -1)
        if(type(id) != int):
            print("No tasks are skipped")
            return(False)

    # toggle skip of task
    tasks[id]['skip'] = False

    # write data
    data_manupulation.write()

    return(True)

def get_first(d: dict, step=1):
    '''
    get first task that matches given key:value
    '''

    def check(i, key):
        return(tasks[i][key] == d[key])
    for i in range(len(tasks))[::step]:
        matches = [check(i, key) for key in d]
        if(all(matches)):
            return(i)
    return(False)
 
def get_next(given_time):
    '''
    get the ID where a task will fit based on it's time
    '''

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

def save_todo(id, a_id=None, every=False):
    '''
    save a task to todo list
    '''

    # save every tasks
    if(every):
        for i in range(len(tasks)):
            save_todo(i, a_id=a_id, every=False)
    
    # use the last task if no ID is provided
    if(not(type(id)==int)):
        id = len(tasks)-1

    # add task to todo
    todo.add(a_id, tasks[id]['name'], tasks[id]['duration'])

    return(True)


def load_todo(id, a_id, every=False):
    '''
    load a task from todo list
    '''

    # load every tasks
    if(every):
        for i in range(len(todo.todo)):
            load_todo(i, a_id=a_id, every=False)

    # if todo list is empty then exist
    if(not(todo.todo)):
        print("Todo list is empty")
        return(False)


    # use the first task in todo list if no ID is provided
    if(not(type(id)==int)):
        id = 0

    # add task to data
    create(a_id, todo.todo[id]['name'], todo.todo[id]['duration'])

    # remove task from todo list
    todo.remove(id)

def copy_todo_yesterday():
    '''
    copy all undone tasks from yesterday's data to todo list
    '''

    try:
        with open(paths.yesterday_path, 'r') as data:
            yesterday = json.load(data)
            for task in yesterday:
                if(not(task['done'])):
                    todo.add(None, task['name'], task['duration'])

    except FileNotFoundError:
        print("There is no Data file for Yesterday's tasks. Yesterday's data file is only generated when newday function is called.")


