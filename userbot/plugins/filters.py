import datetime
import os
import time
import dill
import re
from typing import Dict, List, Tuple
import json
from telethon.tl import functions, types

from userbot import client
from userbot.utils.helpers import get_chat_link
from userbot.utils.events import NewMessage
from telethon.events import StopPropagation
import time
from userbot.plugins import plugins_data
from userbot.utils.helpers import _humanfriendly_seconds, get_chat_link

plugin_category = 'filter'
if not os.path.exists('filters.json'):
    with open('filters.json', 'w') as f:
        data = {}
        f.write(json.dumps(data))
        
@client.onMessage(
    command=("`addfilter` `[Filtro] [Testo]` - `Aggiunti un filtro`", plugin_category),
    outgoing=True, regex=r"addfilter(?: |$)(.+)?$"
)       
async def addfilter(event: NewMessage.Event) -> None: 
    match = event.matches[0].group(1)
    if match:
        arg = match.split(" ")
        with open('filters.json') as json_file:
            data_read = json.load(json_file)
        if len(arg[0]) > 1:
            if len(arg[1]) > 1:
                command = arg[0]
                if command not in data_read:
                    filter_text = match.partition(arg[0])[2]
                    filter_text = filter_text.partition(" ")[2]
                    with open('filters.json', 'w') as f:
                        data = data_read
                        data[command] = filter_text
                        f.write(json.dumps(data))
                        await event.edit(f"✅ **Filtro `{command}` aggiunto ✅**")
                else:
                    await event.edit(f"**❌ Il filtro `{command}` è già impostato!**")                    
        else:
            await event.edit("**❗️ Devi inserire il testo del filtro!**")    
    else:
        await event.edit("**❗️ Utilizzo corretto:** `.addfilter [Filtro] [Testo]`")               
           
           
@client.onMessage(
    command=("`delfilter` `[Filtro]` - `Rimuovi un filtro`", plugin_category),
    outgoing=True, regex=r"(?:delfilter|removefilter)(?: |$)(.+)?$"
)       
async def delfilter(event: NewMessage.Event) -> None: 
    match = event.matches[0].group(1)
    arg = match.split(" ")
    if match:
        with open('filters.json') as json_file:
            data_read = json.load(json_file)
        command = arg[0]
        if command in data_read:
            with open('filters.json', 'w') as f:
                data = data_read
                del data[command]
                f.write(json.dumps(data))
                await event.edit(f"🚫 **Filtro `{command}` rimosso 🚫**")  
        else:
            await event.edit(f"**❌ Il filtro `{command}` non esiste!**")  
    else:
        await event.edit(f"**❗️ Devi inserire il nome del filtro da eliminare!**") 
                
           
@client.onMessage(outgoing=True, edited=False)
async def listner(event: NewMessage.Event) -> None: 
    with open('filters.json') as json_file:
        data_read = json.load(json_file)
    text = event.message.text
    arg = text.split(" ")
    if arg[0] in data_read:
        await event.delete()
        await event.respond(data_read[arg[0]]) 
    
@client.onMessage(
    command=("`filterlist` `Permette di vedere la lista filtri`", plugin_category),
    outgoing=True, regex=r"(?:filterlist|filters)(?: |$)(.+)?$"
)       
async def filterlist(event: NewMessage.Event) -> None: 
    with open('filters.json') as json_file:
        data_read = json.load(json_file)
    if len(data_read) != 0:
        output = "**📯 Filtri attivi:**\n\n"
        for filter_ in data_read:    
            output += f"👉  `{filter_}`    -    `{data_read[filter_]}`\n"
        await event.edit(output)    
    else:
        await event.edit("**💢 Nessun filtro impostato**")
        
        
