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
import re

import requests
from googletrans import Translator
from userbot import client
from userbot.core.events import NewMessage
from userbot.plugins.functions.functions import time_formatter as t


airing_query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        episodes
        title {
          romaji
          english
          native
        }
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        }
      }
    }
    """

anime_query = """
   query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
"""
plugin_category = 'anime'

manga_query = """
query ($id: Int,$search: String) {
      Media (id: $id, type: MANGA,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""


async def callAPI(search_str):
    query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          chapters
          volumes
          season
          type
          format
          status
          duration
          averageScore
          genres
          bannerImage
      }
    }
    """
    variables = {"search": search_str}
    url = "https://graphql.anilist.co"
    response = requests.post(
        url, json={"query": query, "variables": variables})
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
            airing_time_final = t(airing_time)
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
            durata = "{} ore, {} minuti".format(
                str(ore).split('.')[0], minuti)
    else:
        durata = f"{jsonData['duration']} minuti"
    msg += f"\n**• Durata**: `{durata}`\n\n"
    descrizione = translator.translate(jsonData['description'], dest='it')
    descrizione = descrizione.text
    descrizione = descrizione.replace('(Fonte: Anime News Network)', '')
    cat = f"{descrizione}"
    msg += "__" + re.sub("<br>", "\n", cat) + "__"
    return msg

url = "https://graphql.anilist.co"


@client.createCommand(
    command=("manga [Manga]", plugin_category),
    outgoing=True, regex="(?:manga)(?: |$)(.+)?$"
)
async def manga(event: NewMessage.Event) -> None:
    translator = Translator()
    if event.fwd_from:
        return
    search = event.matches[0].group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    variables = {"search": search}
    json = (
        requests.post(url, json={"query": manga_query, "variables": variables})
        .json()["data"]
        .get("Media", None)
    )
    ms_g = ""
    if json:
        title, title_native = json["title"].get("romaji", False), json["title"].get(
            "native", False
        )
        start_date, status, score = (
            json["startDate"].get("year", False),
            json.get("status", False),
            json.get("averageScore", False),
        )
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f" (`{title_native}`)"
        if start_date:
            ms_g += f"\n\n**Anno di inizio** - `{start_date}`"
        if status:
            stato = translator.translate(status, dest='it')
            stato = stato.text
            stato = stato.capitalize()
            ms_g += f"\n**Stato** - `{stato}`"
        if score:
            ms_g += f"\n**Punteggio** - `{score}%`"
        ms_g += "\n**Genere** - "
        for x in json.get("genres", []):
            genere = translator.translate(x, dest='it')
            genere = genere.text
            ms_g += f"`{genere}` - "
        ms_g = ms_g[:-2]
        image = json.get("bannerImage", False)
        descrizione = translator.translate(
            json.get('description', None), dest='it')
        descrizione = descrizione.text
        ms_g += f"\n\n__{descrizione}__"
        ms_g = (
            ms_g.replace("<br>", "\n")
            .replace("</br>", "")
            .replace("<i>", "")
            .replace("</i>", "")
        )
        if image:
            try:
                await event.client.send_file(
                    event.chat_id,
                    image,
                    caption=ms_g,
                    parse_mode="md",
                    reply_to=reply_to_id,
                )
                await event.delete()
            except BaseException:
                pass
        else:
            await event.edit(ms_g)


@client.createCommand(
    command=("anime [Anime]", plugin_category),
    outgoing=True, regex="(?:anime)(?: |$)(.+)?$"
)
async def anilist(event: NewMessage.Event) -> None:
    match = event.matches[0].group(1)
    if match:
        await event.edit("__Sto cercando..attendi qualche istante...__")
        variables = {"search": match}
        json = (
            requests.post(
                url, json={"query": anime_query, "variables": variables})
            .json()["data"]
            .get("Media", None)
        )
        image = json.get("bannerImage", False)
        api = await callAPI(match)
        js = await formatJSON(api, match)
        await event.edit("__Dati raccolti..Sto costruendo il messaggio__")
        if image:
            try:
                await event.client.send_file(
                    event.chat_id,
                    image,
                    caption=js,
                    parse_mode="md",
                )
                await event.delete()
            except BaseException:
                await event.edit(js, link_preview=True)
        else:
            await event.edit(js, link_preview=True)
        await event.delete()
    else:
        await event.edit("__Devi inserire il nome di un anime!__")
