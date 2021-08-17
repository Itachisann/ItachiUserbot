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

from userbot import client
from userbot.core.events import NewMessage

plugin_category = 'filter'


@client.createCommand(
    command=("addfilter [Filtro] [Testo]", plugin_category),
    outgoing=True, regex=r"addfilter(?: |$)(.+)?$"
)
async def addfilter(event: NewMessage.Event) -> None:
    match = event.matches[0].group(1)
    if match:
        arg = match.split(" ")
        with open('userbot/databasefilters.json', encoding="utf8") as json_file:
            data_read = json.load(json_file)
        if len(arg[0]) > 1:
            if len(arg[1]) > 1:
                command = arg[0]
                if command not in data_read:
                    filter_text = match.partition(arg[0])[2]
                    filter_text = filter_text.partition(" ")[2]
                    with open('userbot/databasefilters.json', 'w', encoding='utf8') as f:
                        data = data_read
                        data[command] = filter_text
                        f.write(json.dumps(data, ensure_ascii=False))
                        await event.edit(f"✅ **Filtro `{command}` aggiunto ✅**")
                else:
                    await event.edit(f"**❌ Il filtro `{command}` è già impostato!**")
        else:
            await event.edit("**❗️ Devi inserire il testo del filtro!**")
    else:
        await event.edit("**❗️ Utilizzo corretto:** `.addfilter [Filtro] [Testo]`")


@client.createCommand(
    command=("delfilter [Filtro]", plugin_category),
    outgoing=True, regex=r"(?:delfilter|unfilter)(?: |$)(.+)?$"
)
async def delfilter(event: NewMessage.Event) -> None:
    match = event.matches[0].group(1)
    arg = match.split(" ")
    if match:
        with open('userbot/databasefilters.json', encoding="utf8") as json_file:
            data_read = json.load(json_file)
        command = arg[0]
        if command in data_read:
            with open('userbot/databasefilters.json', 'w') as f:
                data = data_read
                del data[command]
                f.write(json.dumps(data))
                await event.edit(f"🚫 **Filtro `{command}` rimosso 🚫**")
        else:
            await event.edit(f"**❌ Il filtro `{command}` non esiste!**")
    else:
        await event.edit(f"**❗️ Devi inserire il nome del filtro da eliminare!**")


@client.createCommand(outgoing=True, edited=False)
async def listner(event: NewMessage.Event) -> None:
    with open('userbot/databasefilters.json', encoding="utf8") as json_file:
        data_read = json.load(json_file)
    text = event.message.text
    arg = text.split(" ")
    if arg[0] in data_read:
        await event.delete()
        await event.respond(data_read[arg[0]])


@client.createCommand(
    command=("filterlist", plugin_category),
    outgoing=True, regex=r"(?:filterlist|filters)(?: |$)(.+)?$"
)
async def filterlist(event: NewMessage.Event) -> None:
    with open('userbot/databasefilters.json') as json_file:
        data_read = json.load(json_file)
    if len(data_read) != 0:
        output = "**📯 Filtri attivi:**\n\n"
        for filter_ in data_read:
            output += f"👉  `{filter_}`    -    `{data_read[filter_]}`\n"
        await event.edit(output)
    else:
        await event.edit("**💢 Nessun filtro impostato**")
