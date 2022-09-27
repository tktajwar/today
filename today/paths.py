import os

# where today directory will be
path = os.path.expanduser('~')
# today directory
path = os.path.join(path, '.today')

# theme directory
themes_path = os.path.join(path, 'themes')

# path where files are saved
save_path = os.path.join(path, 'saves')

# path to each files
data_path = os.path.join(path, "data.json")
settings_path = os.path.join(path, "settings.json")
purged_path = os.path.join(path, "purged.json")
yesterday_path = os.path.join(path, "yesterday.json")
notes_path = os.path.join(path, 'notes.json')
todo_path = os.path.join(path, 'todo.json')

# where the app is stored/installed
dir_path = os.path.dirname(__file__)

# source of themes
themes_source = os.path.join(dir_path, 'themes')

def check_and_create():
    '''
    create necessary directories if they do not exist
    '''

    # root directory
    if(not(os.path.exists(path))):
        print(f"creating directory: {path}")
        os.makedirs(path)

    # theme directory
    if(not(os.path.exists(themes_path))):
        os.makedirs(themes_path)

    # save directory (where saved datas will be)
    if(not(os.path.exists(save_path))):
        os.makedirs(save_path)
