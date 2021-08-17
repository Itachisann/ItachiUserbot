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


from userbot import client
from userbot.core.events import NewMessage

plugin_category = 'tagall'


@client.createCommand(
    command=("tagall", plugin_category),
    outgoing=True, regex=r"tagall(?: |$)(.*)"
)
async def tagall(event: NewMessage.Event) -> None:
    if event.is_group or event.is_channel:
        await event.delete()
        if event.fwd_from:
            return
        mentions = "__Ho taggato tutti__"
        chat = await event.get_input_chat()
        async for x in event.client.iter_participants(chat, 100):
            mentions += f"[\u2063](tg://user?id={x.id})"
        await event.answer(mentions, reply=True)
