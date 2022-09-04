import json

name = 'sunrise'
theme = {
        'highlight': {
            'id': '\33[91m',
            'header': '\33[4m\33[95m',
            'done': '\33[32m',
            'skip': '\33[90m',
            'undone': {
                'even': '\33[93m',
                'odd': '\33[33m'
                },
            'next': {
                'col': '\33[30m\33[103m',
                'pointer': '*',
            },
        },
        'escape': '\33[0m',
    }

path = 'themes/' + name + '.json'
with open(path, 'w') as data:
    json.dump(theme, data)
