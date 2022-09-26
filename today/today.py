#!/usr/bin/env python3
# import
import argparse

from . import task_manupulation
from . import data_manupulation
from . import settings_manupulation
from . import notes
from . import time_formatting

def parse_arguments(args, a_id=None, a_name=None, a_duration=None, a_st=None, a_times=1, inc=0):
    '''
    argument parsing function
    '''

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
        task_manupulation.task_skip(a_id)

    # task unskip
    elif(args.us):
        task_manupulation.task_unskip(a_id)

    # task modify
    elif(type(args.m)==int):
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
    elif(args.sn):
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
    '''
    main function
    '''

    # parse user arguments
    parser = argparse.ArgumentParser("a day planner")

    ## argument groups
    args_task = parser.add_argument_group("Basic Task and Data")
    args_task_excl = args_task.add_mutually_exclusive_group()

    args_data = parser.add_argument_group("Advanced Data")
    args_data_excl = args_data.add_mutually_exclusive_group()

    args_extra = parser.add_argument_group("Extra")

    args_recursion = parser.add_argument_group("Recursion")

    args_settings = parser.add_argument_group("Settings")
    args_settings_excl = args_settings.add_mutually_exclusive_group()

    args_note = parser.add_argument_group("Notes")
    args_note_excl = args_note.add_mutually_exclusive_group()

    args_file = parser.add_argument_group("File")
    args_file_excl = args_file.add_mutually_exclusive_group()

    ## positional arguments
    parser.add_argument('arguments', metavar='ID Name Duration', nargs='*', help='[int] [str] [time]')

    ## task manupulation arguments
    args_task_excl.add_argument('-a', action='store_true', help='add/append a new Task [ID][Name][Duration]')
    args_task_excl.add_argument('-d', action='store_true', help='mark done [ID]')
    args_task_excl.add_argument('-u', action='store_true', help='mark undone [ID]')
    args_task_excl.add_argument('-r', action='store_true', help='remove [ID]')
    args_task_excl.add_argument('-s', action='store_true', help='skip [ID]')
    args_task_excl.add_argument('-us', action='store_true', help='unskip [ID]')
    args_task_excl.add_argument('-m', metavar='[ID]',  action='store', type=int, help='modify [ID] [Name] [Duration]')
    args_task_excl.add_argument('-D', action='store_true', help='mark all tasks done')
    args_task_excl.add_argument('-U', action='store_true', help='mark all tasks undone')

    ## advanced data manupulation arguments
    args_data_excl.add_argument('-p', action='store_true', help='purge Task Data')
    args_data_excl.add_argument('-v', action='store_true', help='retrieve from Purged Task Data')
    args_data_excl.add_argument('-sn', action='store_true', help='stat a new day')
    args_data_excl.add_argument('-ys', action='store_true', help='show yesterday')

    ## extra info arguments
    args_extra.add_argument('-st', metavar='[time]', action='store', type=str, help='Task start time')

    ##  recursion arguments
    args_recursion.add_argument('-t', metavar='[int]', action='store', type=int, help='do it this number of times')
    args_recursion.add_argument('-inc', action='store_true', help='increment ID by 1 after each time')

    ## settings manupulation arguments
    args_settings_excl.add_argument('-c', action='store_true', help='configure settings')
    args_settings_excl.add_argument('-ct', action='store_true', help='change theme')

    ## notes manupulation arguments
    args_note_excl.add_argument('-ns', action='store_true', help='show notes')
    args_note_excl.add_argument('-na', action='store_true', help='add note')
    args_note_excl.add_argument('-nx', action='store_true', help='delete note [ID]')

    ## file management arguments
    args_file_excl.add_argument('-xs', metavar='[filename]', action='store', type=str, help='save')
    args_file_excl.add_argument('-xl', metavar='[filename]', action='store', type=str, help='load')
    args_file_excl.add_argument('-xx', metavar='[filename]', action='store', type=str, help='delete')
    args_file_excl.add_argument('-ls', action='store_true', help='list files')

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
