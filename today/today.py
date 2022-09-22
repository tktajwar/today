#!/usr/bin/env python3
# import
import argparse

from . import task_manupulation
from . import data_manupulation
from . import settings_manupulation
from . import notes
from . import time_formatting

# argument parsing function
def parse_arguments(args, a_id=None, a_name=None, a_duration=None, a_st=None, a_times=1, inc=0):
    # if the number of times left for this function to run is less than 1
    if(a_times < 1):
        return(False)
    # task add
    if(args.a):
        task_manupulation.create(a_id, a_name, a_duration, start_at=a_st)
    # task done
    elif(args.d):
        task_manupulation.task_do(a_id)
    # task undo
    elif(args.u):
        task_manupulation.task_undo(a_id)
    # task remove
    elif(args.r):
        task_manupulation.task_remove(a_id)
    # task skip
    elif(args.s):
        task_manupulation.task_toggle_skip(a_id)
    # task modify
    elif(args.m):
        task_manupulation.task_modify(args.m, a_id, a_name, a_duration, a_st)
    # task done all
    elif(args.D):
        task_manupulation.task_do_all()
    # task undo all
    elif(args.U):
        task_manupulation.task_undo_all()
    # data purge
    elif(args.p):
        data_manupulation.purge()
    # data retrieve
    elif(args.v):
        data_manupulation.retrieve()
    # data newday
    elif(args.aa):
        data_manupulation.newday()
    # data yesterday
    elif(args.ys):
        task_manupulation.display_yesterday(a_id)
    # settings configure
    elif(args.c):
        settings_manupulation.change()
    # settings theme change
    elif(args.ct):
        settings_manupulation.change_theme()
    # notes show
    elif(args.ns):
        notes.show(a_id)
    # notes add
    elif(args.na):
        notes.add(a_name, a_id)
    # notes remove
    elif(args.nx):
        notes.remove(a_id)
    # data save file
    elif(args.xs):
        data_manupulation.save(args.xs)
    # dat load file
    elif(args.xl):
        data_manupulation.load(args.xl)
    # data delete file
    elif(args.xx):
        data_manupulation.delete(args.xx)
    # data list files
    elif(args.ls):
        data_manupulation.list()
    # task display
    else:
        task_manupulation.display_today(a_id)

    # run again with ID incremented/decremented by increment amount and times decrmented by 1
    if(type(a_id)==int):
        a_id += inc
    a_times -= 1
    parse_arguments(args, a_id, a_name, a_duration, a_st, a_times=a_times, inc=inc)

    return(True)


# main
def main():
    # parse user arguments
    parser = argparse.ArgumentParser("plan and execute your day in an organised way")

    ## argument groups
    args_task = parser.add_argument_group("Basic Task and Data")
    args_adv = parser.add_argument_group("Advanced Data")
    args_extra = parser.add_argument_group("Extra")
    args_recursion = parser.add_argument_group("Recursion")
    args_settings = parser.add_argument_group("Settings")
    args_note = parser.add_argument_group("Notes")
    args_file = parser.add_argument_group("File")

    ## positional arguments
    parser.add_argument('arguments', metavar='ID Name Duration', nargs='*', help='[int] [str] [time]')

    ## task manupulation arguments
    args_task.add_argument('-a', action='store_true', help='add/append a new Task [?ID][Name][Duration]')
    args_task.add_argument('-d', action='store_true', help='mark a task as done [ID]')
    args_task.add_argument('-u', action='store_true', help='mark a task as undone [ID]')
    args_task.add_argument('-r', action='store_true', help='remove Task [ID]')
    args_task.add_argument('-s', action='store_true', help='toggle skip of a Task [ID]')
    args_task.add_argument('-m', metavar='[ID]',  action='store', type=int, help='modify task with new arguments')
    args_task.add_argument('-D', action='store_true', help='mark all tasks as done')
    args_task.add_argument('-U', action='store_true', help='mark all tasks as undone')

    ## advanced data manupulation arguments
    args_adv.add_argument('-p', action='store_true', help='purge Task Data')
    args_adv.add_argument('-v', action='store_true', help='retrieve from Purged Task Data')
    args_adv.add_argument('-sn', action='store_true', help='stat a new day')
    args_adv.add_argument('-ys', action='store_true', help='Show Yesterday\'s Data')

    ## extra info arguments
    args_extra.add_argument('-st', metavar='[time]', action='store', type=str, help='what time do you want a task to start')

    ##  recursion arguments
    args_recursion.add_argument('-t', metavar='[int]', action='store', type=int, help='do it this number of times')
    args_recursion.add_argument('-inc', action='store_true', help='increment ID by 1 at the end of each recursion')

    ## settings manupulation arguments
    args_settings.add_argument('-c', action='store_true', help='configure settings data')
    args_settings.add_argument('-ct', action='store_true', help='change theme')

    ## notes manupulation arguments
    args_note.add_argument('-ns', action='store_true', help='show notes')
    args_note.add_argument('-na', action='store_true', help='add a new note')
    args_note.add_argument('-nx', action='store_true', help='delete a note [ID]')

    ## file management arguments
    args_file.add_argument('-xs', metavar='[filename]', action='store', type=str, help='save to a file')
    args_file.add_argument('-xl', metavar='[filename]', action='store', type=str, help='load from a file')
    args_file.add_argument('-xx', metavar='[filename]', action='store', type=str, help='delete a file')
    args_file.add_argument('-ls', action='store_true', help='list saved files')

    ##
    args = parser.parse_args()

    # number of times the action will be run
    a_times = 1
    if(args.t):
        a_times = args.t

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
    a_st = args.st 
    if(a_st):
        if(a_st == '-1'):
            a_st = -1
        else:
            a_st = time_formatting.to_min(a_st)

    # increment
    inc = 1 if args.inc else 0

    parse_arguments(args=args, a_id=a_id, a_name=a_name, a_duration=a_duration, a_st=a_st, a_times=a_times, inc=inc)

    
if __name__ == "__main__":
    main()
