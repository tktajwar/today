import json

name = 'matrix'
theme = {
        'highlight': {
            'id': '\33[92',
            'header': '\33[92m',
            'done': '\33[32m',
            'skip': '\33[30m',
            'undone': {
                'even': '\33[40m\33[92m',
                'odd': '\33[40m\33[92m'
                },
            'next': {
                'col': '\33[30m\33[102m',
                'pointer': '\33[5m<---',
            },
        },
        'escape': '\33[0m',
    }

path = 'themes/' + name + '.json'
with open(path, 'w') as data:
    json.dump(theme, data)
