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


from userbot.core.events import NewMessage
import json
import re

import requests
from googletrans import Translator
from ..functions.query import airing_query, api_query


async def get_rights(
    event: NewMessage.Event,
    change_info: bool = False,
    post_messages: bool = False,
    edit_messages: bool = False,
    delete_messages: bool = False,
    ban_users: bool = False,
    invite_users: bool = False,
    pin_messages: bool = False,
    add_admins: bool = False
) -> bool:
    chat = await event.get_chat()
    if chat.creator:
        return True
    rights = {
        'change_info': change_info,
        'post_messages': post_messages,
        'edit_messages': edit_messages,
        'delete_messages': delete_messages,
        'ban_users': ban_users,
        'invite_users': invite_users,
        'pin_messages': pin_messages,
        'add_admins': add_admins
    }
    required_rights = []
    for right, required in rights.items():
        if required:
            required_rights.append(getattr(chat.admin_rights, right, False))

    return all(required_rights)


async def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " giorni, ") if days else "")
        + ((str(hours) + " ore, ") if hours else "")
        + ((str(minutes) + " minuti, ") if minutes else "")
        + ((str(seconds) + " secondi, ") if seconds else "")
        + ((str(milliseconds) + " millisecondi, ") if milliseconds else "")
    )
    return tmp[:-2]

url = "https://graphql.anilist.co"


async def callAPI(search_str):
    variables = {"search": search_str}
    url = "https://graphql.anilist.co"
    response = requests.post(
        url, json={"query": api_query, "variables": variables})
    return response.text


async def formatJSON(outData, search):
    translator = Translator()
    msg = ""
    jsonData = json.loads(outData)
    res = list(jsonData.keys())
    variables = {"search": search}
    response = requests.post(
        url, json={"query": airing_query, "variables": variables}
    ).json()["data"]["Media"]
    if "errors" in res:
        errore = translator.translate(
            jsonData['errors'][0]['message'], dest='it')
        errore = errore.text
        msg += f"**❗️ Errore**: `{errore}`"
        return msg
    jsonData = jsonData["data"]["Media"]
    if "bannerImage" in jsonData.keys():
        msg += f"[〽️]({jsonData['bannerImage']}) "
    else:
        msg += "〽️ "
    title = jsonData["title"]["romaji"]
    link = f"https://anilist.co/anime/{jsonData['id']}"
    msg += f"[{title}]({link})"
    format = translator.translate(jsonData['format'], dest='it')
    format = format.text
    format = format.capitalize()
    msg += f"\n\n**• Tipologia**: `{format}`"
    msg += f"\n**• Genere**: "
    genere = " - ".join([f'`{g}`' for g in jsonData["genres"]])
    genere = translator.translate(genere, dest='it')
    msg += genere.text
    stato = translator.translate(jsonData['status'], dest='it')
    stato = stato.text
    stato = stato.capitalize()
    msg += f"\n**• Stato**: `{stato}`"
    if format != 'Film':
        if response["nextAiringEpisode"]:
            airing_time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
            airing_time_final = time_formatter(airing_time)
            msg += f"\n**• Episodi**: `{response['nextAiringEpisode']['episode']}`\n**  • Prossimo episodio tra**: `{airing_time_final}`"
        else:
            msg += f"\n**• Episodi**: `{response['episodes']}`\n**• Stato**: `N/A`"
    msg += f"\n**• Anno di produzione** : `{jsonData['startDate']['year']}`"
    msg += f"\n**• Punteggio** : `{jsonData['averageScore']}%`"
    if jsonData['duration'] >= 60:
        ore = jsonData['duration'] / 60
        minuti = jsonData['duration'] % 60
        if jsonData['duration'] == 60:
            durata = '1 ora'
        else:
            ore = str(ore).split('.')[0]
            if ore == '1':
                durata = "{} ora, {} minuti".format(
                    ore, minuti)
            else:
                durata = "{} ora, {} minuti".format(
                    ore, minuti)
    else:
        durata = f"{jsonData['duration']} minuti"
    msg += f"\n**• Durata**: `{durata}`\n\n"
    descrizione = translator.translate(jsonData['description'], dest='it')
    descrizione = descrizione.text
    descrizione = descrizione.replace('(Fonte: Anime News Network)', '')
    cat = f"{descrizione}"
    msg += "__" + re.sub("<br>", "\n", cat) + "__"
    return msg


async def async_searcher(
    url: str,
    post: bool = None,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    data: dict = None,
    ssl=None,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
    *args,
    **kwargs,
):
    try:
        import aiohttp
    except ImportError:
        return
    async with aiohttp.ClientSession(headers=headers) as client:
        if post:
            data = await client.post(
                url, json=json, data=data, ssl=ssl, *args, **kwargs
            )
        else:
            data = await client.get(url, params=params, ssl=ssl, *args, **kwargs)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if real:
            return data
        return await data.text()
