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


import inspect

from meval import meval
from userbot import client
from userbot.core.events import NewMessage
from userbot.core.helpers import get_chat_link

plugin_category = "calculator"


@client.createCommand(
    command=("calc [Operazioni]", plugin_category),
    outgoing=True, regex=r"calc(?: |$|\n)([\s\S]*)"
)
async def calc(event: NewMessage.Event) -> None:
    expression = event.matches[0].group(1).strip()
    reply = await event.get_reply_message()
    if not expression:
        await event.answer("__Inserisci parametri validi per fare operazioni!__")
        return

    try:
        result = await meval(
            expression, globals(), client=client, event=event, reply=reply
        )
    except Exception as e:
        await event.answer(
            f"`Operazione non riuscita.`", reply=True)
        return

    extra = await get_chat_link(event, event.id)
    if result:
        if hasattr(result, 'stringify'):
            if inspect.isawaitable(result):
                result = await result.stringify()
            else:
                result = result.stringify()
    result = str(result) if result else "Questa è una risposta ovvia.."
    await event.answer(
        "```Risultato: " + result + "```",
        log=("eval", f"Successfully evaluated {expression} in {extra}!"),
        reply=True
    )
