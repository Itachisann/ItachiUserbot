import json
import os


def generateFile():
    if not os.path.exists('Database'):
        os.mkdir('Database')

    if not os.path.exists('userbot/databasefilters.json'):
        with open('userbot/databasefilters.json', 'w', encoding="utf8") as f:
            data = {}
            f.write(json.dumps(data))

    if not os.path.exists('userbot/databasemuted.json'):
        with open('userbot/databasemuted.json', 'w', encoding="utf8") as f:
            data = {}
            data['muted_list'] = []
            f.write(json.dumps(data))

    if not os.path.exists('userbot/databasedatabase.json'):
        with open('userbot/databasedatabase.json', 'w') as f:
            data = {}
            data['approved_users'] = []
            data['approved_username'] = []
            f.write(json.dumps(data))
