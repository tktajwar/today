import json

name = 'sunrise'
theme = {
        'highlight': {
            'id': '\33[91m',
            'header': '\33[4m\33[95m',
            'done': '\33[32m',
            'skip': '\33[90m',
            'undone': '\33[93m',
            'next': {
                'col': '\33[100m',
                'pointer': None,
            },
        },
        'escape': '\33[0m',
    }

path = 'themes/' + name + '.json'
with open(path, 'w') as data:
    json.dump(theme, data)
