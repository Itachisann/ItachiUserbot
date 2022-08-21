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


from pydantic import NotNoneError
from userbot import client
from userbot.core.events import NewMessage
from userbot.plugins.functions.functions import async_searcher

plugin_category = 'AI'
ai_mode = False
chat_id = None


@client.createCommand(
    command=("chatbot", plugin_category),
    outgoing=True, regex=r"chatbot(?: |$)(.+)?$"
)
async def ai_response(message):
    chatbot_base = "https://kukiapi.xyz/api/apikey=ULTROIDUSERBOT/Ultroid/{}/message={}"
    req_link = chatbot_base.format(
        'io',
        message,
    )
    try:
        return (await async_searcher(req_link, re_json=True)).get("reply")
    except Exception:
        return


@client.createCommand(
    command=("chatbot", plugin_category),
    outgoing=True, regex=r"chatbot(?: |$)(.+)?$"
)
async def ai(event: NewMessage.Event) -> None:
    global ai_mode
    global chat_id
    if ai_mode == False:
        await event.edit('__🧠 AI ChatBot attivato!__')
        ai_mode = True
        chat_id = event.chat_id
    else:
        await event.edit('__❌ AI ChatBot disattivato!__')
        ai_mode = False
        chat_id = None


@client.createCommand(incoming=True, edited=False)
async def listner(event: NewMessage.Event) -> None:
    global chat_id
    if (chat_id != event.chat_id):
        return
    global ai_mode
    if ai_mode == True:
        if event.reply_to:
            message = (await event.get_reply_message()).message
        else:
            message = event.text
        reply_ = await ai_response(message=message)
        await event.resanswer(reply_, reply=True)
