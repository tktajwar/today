import json

from . import paths
from . import theme_manupulation

notes_path = paths.notes_path

# show notes
def show(id=None):
    notes = read() # load notes
    theme = theme_manupulation.load() # load theme

    # show individual note
    if(id):
        print(notes[id])
        return(True)

    # show all the notes
    for i in range(len(notes)):
        print(f"{theme['highlight']['id']}{i}{theme['escape']}: {notes[i]}")
    return(True)

# read note file
def write(notes):
    with open(notes_path, 'w') as data:
        json.dump(notes, data)

# read note file
def read():
    notes=[]

    try:
        with open(notes_path, 'r') as data:
            notes = json.load(data)

    except FileNotFoundError:
        print('Notes file does not exist. Creating a new one.')
        write(notes)
        return([])
    return(notes)

# add a new note
def add(note, id=None):
    notes = read()

    if(type(id)==int):
        notes.insert(note, id)

    else:
        notes.append(note)
    write(notes)

# remove a note
def remove(id=None):
    notes = read()

    if(type(id)==int):
        notes.pop(id)

    else:
        notes.pop()
    write(notes)
