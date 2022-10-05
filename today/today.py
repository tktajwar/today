#!/usr/bin/env python3
# import
import argparse
from sys import argv

from . import task_manupulation
from . import data_manupulation
from . import settings_manupulation
from . import todo
from . import time_formatting

def parse_arguments(args, a_id=None, a_name=None, a_duration=None, a_st=None, a_time_start=None, a_times=1, inc=0):
    '''
    argument parsing function
    '''
    init_id = a_id

    for i in range(a_times):
        # make ID = intial ID + increment value * (iteration number-1)
        if(type(a_id)==int):
            a_id = init_id + inc*i

        # task add
        if(args.a):
            task_manupulation.create(a_id, a_name, a_duration, start_at=a_st)

        # task done
        elif(args.d):
            if(args.E): # every
                task_manupulation.task_do_all()
            else:
                task_manupulation.task_do(a_id)

        # task undo
        elif(args.D):
            if(args.E): # every
                task_manupulation.task_undo_all()
            else:
                task_manupulation.task_undo(a_id)

        # task remove
        elif(args.r):
            task_manupulation.task_remove(a_id, every=args.E)

        # task skip
        elif(args.s):
            task_manupulation.task_skip(a_id, every=args.E)

        # task unskip
        elif(args.S):
            task_manupulation.task_unskip(a_id, every=args.E)

        # task modify
        elif(type(args.m)==int):
            task_manupulation.task_modify(args.m, a_id, a_name, a_duration, a_st, every=args.E)

        # data purge
        if(args.p):
            data_manupulation.purge()

        # data retrieve
        elif(args.P):
            data_manupulation.retrieve()

        # data newday
        elif(args.aa):
            data_manupulation.newday()

        # data yesterday
        elif(args.yy):
            task_manupulation.display_yesterday(a_id)

        # todo add
        if(args.A):
            todo.add(a_id, a_name, a_duration)

        # todo remove
        elif(args.R):
            todo.remove(a_id, every=args.E)

        # todo save
        elif(type(args.C)==int):
            task_manupulation.save_todo(args.C, a_id, every=args.E)

        # todo load 
        elif(type(args.L)==int):
            task_manupulation.load_todo(args.L, a_id, every=args.E)

        # todo load undone from yesterday
        elif(args.CY):
            task_manupulation.copy_todo_yesterday()

        # settings set day start
        elif(type(a_time_start)==int):
            settings_manupulation.change_time(a_time_start)

       # settings configure
        if(args.conf):
            settings_manupulation.change()

        # settings theme change
        elif(args.theme):
            settings_manupulation.change_theme()
        
        # data save file
        if(args.xs):
            data_manupulation.save(args.xs)

        # data load file
        elif(args.xl):
            data_manupulation.load(args.xl)

        # data delete file
        elif(args.xx):
            data_manupulation.delete(args.xx, every=args.E)

        # data list files
        elif(args.ls):
            data_manupulation.list()

        # task display
        if(len(argv)<=1 or args.y):
            task_manupulation.display_today(a_id)

    return(True)


# main
def main():
    '''
    main function
    '''

    # parse user arguments
    parser = argparse.ArgumentParser("today [Positoinal Arguments] [Optional Arguments]")

    ## argument groups
    args_task = parser.add_argument_group("Basic Task and Data")
    args_task_excl = args_task.add_mutually_exclusive_group()

    args_data = parser.add_argument_group("Advanced Data")
    args_data_excl = args_data.add_mutually_exclusive_group()

    args_extra = parser.add_argument_group("Extra")

    args_todo = parser.add_argument_group("Todo List")
    args_todo_excl = args_todo.add_mutually_exclusive_group()

    args_mod = parser.add_argument_group("Modifiers")
    args_mod_iteration_excl = args_mod.add_mutually_exclusive_group()

    args_settings = parser.add_argument_group("Settings")
    args_settings_excl = args_settings.add_mutually_exclusive_group()

    args_file = parser.add_argument_group("File")
    args_file_excl = args_file.add_mutually_exclusive_group()

    ## positional arguments
    parser.add_argument('arguments', metavar='ID Name Duration', nargs='*', help='[int] [str] [time]')

    ## task manupulation arguments
    args_task_excl.add_argument('-a', action='store_true', help='add/append Task [ID][Name][Duration]')
    args_task_excl.add_argument('-d', action='store_true', help='mark done [ID]')
    args_task_excl.add_argument('-D', action='store_true', help='mark undone [ID]')
    args_task_excl.add_argument('-r', action='store_true', help='remove [ID]')
    args_task_excl.add_argument('-s', action='store_true', help='skip [ID]')
    args_task_excl.add_argument('-S', action='store_true', help='unskip [ID]')
    args_task_excl.add_argument('-m', metavar='[ID]',  action='store', type=int, help='modify [New ID] [New Name] [New Duration]')
    args_task.add_argument('-y', action='store_true', help='display Tasks')

    ## advanced data manupulation arguments
    args_data_excl.add_argument('-p', action='store_true', help='purge Task Data')
    args_data_excl.add_argument('-P', action='store_true', help='retrieve purged Task Data')
    args_data_excl.add_argument('--aa', action='store_true', help='stat a new day')
    args_data_excl.add_argument('--yy', action='store_true', help='display yesterday')

    ## extra info arguments
    args_extra.add_argument('-t', metavar='[time]', action='store', type=str, help='Task start time')

    # todo list arguments
    args_todo_excl.add_argument('-A', action='store_true', help='add a new task to todo list [ID] [Name] [Duration]')
    args_todo_excl.add_argument('-R', action='store_true', help='remove a task from todo list [ID]')
    args_todo_excl.add_argument('-C', metavar='[ID]', action='store', type=int, help='copy a task to todo list')
    args_todo_excl.add_argument('-L', metavar='[ID]', action='store', type=int, help='load a task from todo list')
    args_todo_excl.add_argument('--CY', action='store_true', help='copy yesterday\'s undone tasks to todo list')

    ## modifier arguments
    args_mod.add_argument('-E', action='store_true', help='do action for every Tasks')
    args_mod_iteration_excl.add_argument('-i', metavar='[int]', action='store', type=int, help='iterate this number of times')
    args_mod_iteration_excl.add_argument('-I', metavar='[int]', action='store', type=int, help='iterate this number of times with incrementing ID')

    ## settings manupulation arguments
    args_settings_excl.add_argument('-T', metavar='[time]', action='store', type=str, help='day start time')
    args_settings_excl.add_argument('--conf', action='store_true', help='configure settings')
    args_settings_excl.add_argument('--theme', action='store_true', help='change theme')

    ## file management arguments
    args_file_excl.add_argument('--xs', metavar='[filename]', action='store', type=str, help='save')
    args_file_excl.add_argument('--xl', metavar='[filename]', action='store', type=str, help='load')
    args_file_excl.add_argument('--xx', metavar='[filename]', action='store', type=str, help='delete')
    args_file_excl.add_argument('--ls', action='store_true', help='list files')

    ##
    args = parser.parse_args()

    # number of times the action will be run and ID increation
    inc = 0
    a_times = 1
    if(args.i):
        a_times = args.i
    elif(args.I):
        a_times = args.I
        inc = 1

    # get ID, name and duration from user argument
    a_id, a_name, a_duration = None, None, None
    if(args.arguments):
        # if only one argument is passed (ID/Name/Duration)
        if(len(args.arguments) == 1): 
            if(args.arguments[0].isnumeric()):
                a_id = int(args.arguments[0])
            elif(time_formatting.is_duration(args.arguments[0])):
                a_duration = args.arguments[0]
            else:
                a_name = args.arguments[0]
        # first item is numeric (ID + Name and/or Duration)
        elif(args.arguments[0].isnumeric()):
            a_id = int(args.arguments[0])
            # last item is numeric/duration
            if(args.arguments[-1].isnumeric() or time_formatting.is_duration(args.arguments[-1])):
                a_duration = args.arguments[-1]
                # everything in the middle is Name
                if(len(args.arguments)>2):
                    a_name = " ".join(args.arguments[1:-1])
            # if not, everything to the end is Name
            else: 
                a_name = " ".join(args.arguments[1:])
        # (Name and/or Duration)
        else:
            # last item is numeric/duration
            if(args.arguments[-1].isnumeric() or time_formatting.is_duration(args.arguments[-1])):
                a_duration = args.arguments[-1]
                a_name = " ".join(args.arguments[:-1])
            # Name only
            else:
                a_name = " ".join(args.arguments)

    # turn duration into minutes
    if(a_duration):
        a_duration = time_formatting.to_min(a_duration)

    # turn start_at duration into minutes
    a_st = args.t 
    if(a_st):
        if(a_st == '-1'):
            a_st = -1
        else:
            a_st = time_formatting.to_min(a_st)

    # turn time start into minutes
    a_time_start = args.T
    if(a_time_start):
        a_time_start = time_formatting.to_min(a_time_start)

    parse_arguments(args=args, a_id=a_id, a_name=a_name, a_duration=a_duration, a_st=a_st, a_time_start=a_time_start, a_times=a_times, inc=inc)

    
if __name__ == "__main__":
    main()
