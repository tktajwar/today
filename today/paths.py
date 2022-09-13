import os

path = os.path.expanduser('~')
path = os.path.join(path, '.today')
data_path = os.path.join(path, "data.json")
settings_path = os.path.join(path, "settings.json")
purged_path = os.path.join(path, "purged.json")
yesterday_path = os.path.join(path, "yesterday.json")
themes_path = os.path.join(path, 'themes')
notes_path = os.path.join(path, 'notes.json')

dir_path = os.path.dirname(__file__)
themes_source = os.path.join(dir_path, 'themes')

#create root directory if it does not exist
def check_and_create():
    if (not(os.path.exists(path))):
        print(f"creating directory: {path}")
        os.makedirs(path)
    if (not(os.path.exists(themes_path))):
        os.makedirs(themes_path)
