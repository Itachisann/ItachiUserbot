# Itachi Userbot - A telegram userbot.
# Copyright (C) 2021 Itachisann

# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see < https: // www.gnu.org/licenses/>.


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
