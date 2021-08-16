import datetime
import os
import time
import re
from typing import Dict, List, Tuple
import json

from userbot import client
from userbot.core.events import command

if not os.path.exists('filters.json'):
    with open('filters.json', 'w', encoding="utf8") as f:
        data = {}
        f.write(json.dumps(data))

if not os.path.exists('muted.json'):
    with open('muted.json', 'w', encoding="utf8") as f:
        data = {}
        data['muted_list'] = []
        f.write(json.dumps(data))
        
if not os.path.exists('database.json'):
    with open('database.json', 'w') as f:
        data = {}
        data['approved_users'] = []
        data['approved_username'] = []
        f.write(json.dumps(data))
