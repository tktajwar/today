import json

from . import paths
from . import theme_manupulation

notes_path = paths.notes_path

def show(id=None):
    notes = read()
    theme = theme_manupulation.load()
    if(id):
        print(notes[id])
        return(True)
    for i in range(len(notes)):
        print(f"{theme['highlight']['id']}{i}{theme['escape']}: {notes[i]}")

def write(notes):
    with open(notes_path, 'w') as data:
        json.dump(notes, data)

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

def add(note, id=None):
    notes = read()
    if(type(id)==int):
        notes.insert(note, id)
    else:
        notes.append(note)
    write(notes)

def remove(id=None):
    notes = read()
    if(type(id)==int):
        notes.pop(id)
    else:
        notes.pop()
    write(notes)


