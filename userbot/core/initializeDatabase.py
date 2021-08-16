import json
import os


def generateFile():
    if not os.path.exists('Database'):
        os.mkdir('Database')

    if not os.path.exists('Database/filters.json'):
        with open('Database/filters.json', 'w', encoding="utf8") as f:
            data = {}
            f.write(json.dumps(data))

    if not os.path.exists('Database/muted.json'):
        with open('Database/muted.json', 'w', encoding="utf8") as f:
            data = {}
            data['muted_list'] = []
            f.write(json.dumps(data))

    if not os.path.exists('Database/database.json'):
        with open('Database/database.json', 'w') as f:
            data = {}
            data['approved_users'] = []
            data['approved_username'] = []
            f.write(json.dumps(data))
