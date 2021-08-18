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


import requests
from googletrans import Translator
from userbot import client
from userbot.core.events import NewMessage
from userbot.plugins.functions.query import anime_query, manga_query
from userbot.plugins.functions.functions import callAPI, formatJSON

plugin_category = 'anime'

url = "https://graphql.anilist.co"
translator = Translator()


@client.createCommand(
    command=("manga [Manga]", plugin_category),
    outgoing=True, regex="(?:manga)(?: |$)(.+)?$"
)
async def manga(event: NewMessage.Event) -> None:
    if event.fwd_from:
        return
    match = event.matches[0].group(1)
    if match:
        await event.edit(f"__Sto cercando informazioni sul manga `{match}`..attendi qualche istante...__")
        reply_to_id = event.message.id
        if event.reply_to_msg_id:
            reply_to_id = event.reply_to_msg_id
        variables = {"search": match}
        json = (
            requests.post(
                url, json={"query": manga_query, "variables": variables})
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
            await event.edit("__Dati raccolti..Sto costruendo il messaggio__")
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
                    await event.edit(ms_g, link_preview=True)
            else:
                await event.edit(ms_g)
    else:
        await event.edit("__Devi inserire il nome di un manga!__")


@client.createCommand(
    command=("anime [Anime]", plugin_category),
    outgoing=True, regex="(?:anime)(?: |$)(.+)?$"
)
async def anilist(event: NewMessage.Event) -> None:
    match = event.matches[0].group(1)
    if match:
        await event.edit(f"__Sto cercando informazioni sull'anime `{match}`..attendi qualche istante...__")
        variables = {"search": match}
        api = await callAPI(match)
        js = await formatJSON(api, match)
        await event.edit("__Dati raccolti..Sto costruendo il messaggio__")
        json = (
            requests.post(
                url, json={"query": anime_query, "variables": variables})
            .json()["data"]
            .get("Media", None)
        )
        image = json.get("bannerImage", False)
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
