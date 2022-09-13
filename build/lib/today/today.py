#!/usr/bin/env python3
# import
import argparse

from . import task_manupulation
from . import data_manupulation
from . import settings_manupulation
from . import notes
from . import time_formatting

# variables and parsing arguments
## parser
parser = argparse.ArgumentParser('plan and execute your day in an organised way')
##
is_duration = time_formatting.is_duration

# main
def main():
    # parse user arguments
    ## positional arguments
    parser.add_argument('arguments', metavar='Arguments', nargs='*', help='Task ID [int], Name [str], Duration [int]')
    ## positional requiring options
    parser.add_argument('-a', '--add', action='store_true', help='add/append a new Task [?ID][Name][Duration]')
    parser.add_argument('-d', '--done', action='store_true', help='mark a task as done [ID]')
    parser.add_argument('-u', '--undo', action='store_true', help='mark a task as undone [ID]')
    parser.add_argument('-r', '--remove', action='store_true', help='remove Task [ID]')
    parser.add_argument('-t', '--toggle', action='store_true', help='toggle Skip of Task [ID]')
    ## non positional requiring options
    parser.add_argument('-da', '--done-all', action='store_true', help='mark all tasks as done')
    parser.add_argument('-ua', '--undo-all', action='store_true', help='mark all tasks as undone')
    parser.add_argument('-p', '--purge', action='store_true', help='purge Task Data')
    parser.add_argument('-v', '--retrieve', action='store_true', help='retrieve from Purged Task Data')
    parser.add_argument('-n', '--new-day', action='store_true', help='store current Task Data as Yesterday and start a new Day')
    parser.add_argument('-y', '--yesterday', action='store_true', help='Show Yesterday\'s Data')
    parser.add_argument('-c', '--settings', action='store_true', help='configure settings data')
    parser.add_argument('-ct', '--change-theme', action='store_true', help='change theme')
    parser.add_argument('-g', '--read-notes', action='store_true', help='show notes')
    parser.add_argument('-w', '--add_note', action='store_true', help='add a new note')
    parser.add_argument('-x', '--remove-note', action='store_true', help='delete a note')

    ##
    args = parser.parse_args()

    a_id, a_name, a_duration = None, None, None
    if(args.arguments):
        if(len(args.arguments) == 1): # if only one argument is passed then it's either ID or Name
            if(args.arguments[0].isnumeric()):
                a_id = int(args.arguments[0])
            elif(is_duration(args.arguments[0])):
                a_duration = args.arguments[0]
            else:
                a_name = args.arguments[0]
        elif(args.arguments[0].isnumeric()): # ID + Name and/or Duration
            a_id = int(args.arguments[0])
            if(args.arguments[-1].isnumeric() or is_duration(args.arguments[-1])):
                a_duration = args.arguments[-1]
                if(len(args.arguments)>2): # everything in the middle is Name
                    a_name = " ".join(args.arguments[1:-1])
            else: # everything to the end is Name
                a_name = " ".join(args.arguments[1:])
        else: # Name + Duration(*)
            if(args.arguments[-1].isnumeric() or is_duration(args.arguments[-1])): # Name + Duration
                a_duration = args.arguments[-1]
                a_name = " ".join(args.arguments[:-1])
            else: # Name only
                a_name = " ".join(args.arguments)
    if(a_duration):
        a_duration = to_min(a_duration)

    if(args.add):
        task_manupulation.create(a_id, a_name, a_duration)
    elif(args.done):
        task_manupulation.task_do(a_id)
    elif(args.undo):
        task_manupulation.task_undo(a_id)
    elif(args.remove):
        task_manupulation.task_remove(a_id)
    elif(args.toggle):
        task_manupulation.task_toggle_skip(a_id)
    elif(args.done_all):
        task_manupulation.task_do_all()
    elif(args.undo_all):
        task_manupulation.task_undo_all()
    elif(args.purge):
        data_manupulation.purge()
    elif(args.retrieve):
        data_manupulation.retrieve()
    elif(args.new_day):
        data_manupulation.newday()
    elif(args.yesterday):
        task_manupulation.display_yesterday(a_id)
    elif(args.settings):
        settings_manupulation.change()
    elif(args.change_theme):
        settings_manupulation.change_theme()
    elif(args.read_notes):
        notes.show(a_id)
    elif(args.add_note):
        notes.add(a_name, a_id)
    elif(args.remove_note):
        notes.remove(a_id)
    else:
        task_manupulation.display_today(a_id)

if __name__ == "__main__":
    main()