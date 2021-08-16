import datetime
import json
import os
import re
import time
from typing import Dict, List, Tuple

from telethon.tl import types
from userbot import client
from userbot.core.events import NewMessage
from userbot.core.helpers import get_chat_link
from userbot.plugins.functions.functions import get_rights

plugin_category = 'filter'


@client.createCommand(
    command=("mute [Utente]", plugin_category),
    outgoing=True, regex=r"mute(?: |$)(.+)?$"
)
async def mute(event: NewMessage.Event) -> None:
    match = event.matches[0].group(1)
    users = await get_users(event)
    chatid = str(event.chat_id)
    with open('Database/muted.json', encoding="utf8") as json_file:
        data_read = json.load(json_file)
    if event.is_private:
        href = await get_chat_link(event.chat)
        if 'yourself' not in href:
            if chatid not in data_read['muted_list']:
                with open('Database/muted.json', 'w', encoding='utf8') as f:
                    await event.edit("✅ __Hai mutato__ " + href + '!')
                    data = data_read
                    data['muted_list'].append(chatid)
                    f.write(json.dumps(data))
            else:
                await event.edit("💢 " + href + " __è già mutato__")
    else:
        if await get_rights(event, ban_users=True):
            if users:
                for user in users:
                    if chatid not in data_read:
                        await event.edit(f"✅ __Hai mutato con successo __@{user.username}__ in questo gruppo!__")
                        with open('Database/muted.json', 'w', encoding='utf8') as f:
                            data = data_read
                            data[chatid] = [user.id]
                            f.write(json.dumps(data))
                    else:
                        if user.id not in data_read[chatid]:
                            await event.edit(f"✅ __Hai mutato con successo __@{user.username}__ in questo gruppo!__")
                            with open('Database/muted.json', 'w', encoding='utf8') as f:
                                data = data_read
                                data[chatid].append(user.id)
                                f.write(json.dumps(data))
                        else:
                            await event.edit('__💢 Questo utente è già mutato__')
        else:
            await event.edit('__💢 Non hai i permessi necessari per mutare in questo gruppo!__')


@client.createCommand(
    command=("unmute [Utente]", plugin_category),
    outgoing=True, regex=r"unmute(?: |$)(.+)?$"
)
async def unmute(event: NewMessage.Event) -> None:
    match = event.matches[0].group(1)
    users = await get_users(event)
    chatid = str(event.chat_id)
    with open('Database/muted.json', encoding="utf8") as json_file:
        data_read = json.load(json_file)
    if event.is_private:
        href = await get_chat_link(event.chat)
        if 'yourself' not in href:
            if chatid in data_read['muted_list']:
                with open('Database/muted.json', 'w', encoding='utf8') as f:
                    await event.edit(f"✅ __Hai smutato__ " + href + '!')
                    data = data_read
                    data['muted_list'].remove(chatid)
                    f.write(json.dumps(data))
            else:
                await event.edit("💢 " + href + " __è già smutato__")
    else:
        if await get_rights(event, ban_users=True):
            if users:
                for user in users:
                    if chatid not in data_read:
                        await event.edit(f"💢 @{user.username}__ non è mutato!__")
                    else:
                        if user.id in data_read[chatid]:
                            await event.edit(f"✅ __Hai smutato con successo __@{user.username}__ in questo gruppo!__")
                            with open('Database/muted.json', 'w', encoding='utf8') as f:
                                data = data_read
                                data[chatid].remove(user.id)
                                f.write(json.dumps(data))
                        else:
                            await event.edit('__💢 Questo utente non è mutato__')
        else:
            await event.edit('__💢 Non hai i permessi necessari per smutare in questo gruppo!__')


async def get_users(event: NewMessage.Event) -> types.User or None:
    match = event.matches[0].group(1)
    users = []
    if match:
        matches, _ = await client.parse_arguments(match)
        for match in matches:
            try:
                entity = await client.get_entity(match)
                if isinstance(entity, types.User):
                    users.append(entity)
            except (TypeError, ValueError):
                pass
    elif event.is_private and event.out:
        users = [await event.get_chat()]
    elif event.reply_to_msg_id:
        reply = await event.get_reply_message()
        users = [await reply.get_sender()]
    return users


@client.createCommand(incoming=True, edited=False)
async def listner(event: NewMessage.Event) -> None:
    chat_id = str(event.chat_id)
    with open('Database/muted.json', encoding="utf8") as json_file:
        data_read = json.load(json_file)
    if event.is_private:
        if chat_id in data_read['muted_list']:
            await event.delete()
    else:
        sender = await event.get_sender()
        userid = sender.id
        if chat_id in data_read:
            if userid in data_read[chat_id]:
                await event.delete()
