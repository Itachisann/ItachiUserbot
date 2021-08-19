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


import asyncio

from googletrans import Translator
from telethon.tl import functions
from userbot import LOGGER, client
from userbot.core.events import NewMessage

plugin_category = "core"


@client.createCommand(
    command=("spam [Numero messaggi] [Messaggio]", plugin_category),
    outgoing=True, regex=r"spam(?: |$|\n)([\s\S]*)"
)
async def spam(event: NewMessage.Event) -> None:
    arg = event.matches[0].group(1)
    arg_ = arg.split(" ")
    if arg:
        try:
            value = int(arg_[0])
        except ValueError:
            await event.edit('__Devi inserire un numero di messaggi valido!__')
        if type(value) == int:
            if len(arg_[0]) > 1:
                for i in range(0, value, 1):
                    text = arg.partition(arg_[0])[2]
                    await event.respond(text)
            else:
                await event.edit("**❗️ Devi inserire il messaggio!**")
    else:
        await event.edit('**❗️ Utilizzo corretto:** `.spam [Numero messaggi] [Messaggio]`')


@client.createCommand(
    command=("pin", plugin_category),
    outgoing=True, regex=r"pin(?: |$|\n)([\s\S]*)"
)
async def pin(event: NewMessage.Event) -> None:
    if event.fwd_from:
        return
    if event.message.reply_to_msg_id is not None:
        try:
            await client(functions.messages.UpdatePinnedMessageRequest(
                event.chat_id,
                event.message.reply_to_msg_id,
                silent=False
            ))
        except Exception as e:
            await event.edit(str(e))
        else:
            await event.delete()
    else:
        await event.edit("__Rispondi al messaggio da pinnare.__")


@client.createCommand(
    command=("type [Messaggio]", plugin_category),
    outgoing=True, regex=r"type(?: |$|\n)([\s\S]*)"
)
async def typechar(event: NewMessage.Event) -> None:
    if event.fwd_from:
        return
    arg = event.matches[0].group(1)
    typing_symbol = "|"
    DELAY_BETWEEN_EDITS = 0.3
    previous_text = ""
    await event.edit(typing_symbol)
    await asyncio.sleep(DELAY_BETWEEN_EDITS)
    for character in arg:
        previous_text = previous_text + "" + character
        typing_text = previous_text + "" + typing_symbol
        try:
            await event.edit(f"`{typing_text}`")
        except Exception as e:
            LOGGER.warn(str(e))
            pass
        await asyncio.sleep(DELAY_BETWEEN_EDITS)
        try:
            await event.edit(f"`{previous_text}`")
        except Exception as e:
            LOGGER.warn(str(e))
            pass
        await asyncio.sleep(DELAY_BETWEEN_EDITS)


@client.createCommand(
    command=("hack", plugin_category),
    outgoing=True, regex=r"hack(?: |$|\n)([\s\S]*)"
)
async def hack(event: NewMessage.Event) -> None:
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 10)
    animation_chars = [
        "**Connettendosi al database di Telegram**",
        "`Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)",
        "`Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package",
        "`Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)",
        "`Hacking... 21%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'",
        "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e",
        "`Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\nStored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b",
        "`Hacking... 84%\n█████████████████████▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\nStored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Accesso consentito...**",
        "`Hacking... 96%\n████████████████████████ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\nStored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Ottimizzando i dati..**",
        "`Hacking... 100%\n█████████████████████████ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\nDownloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\nStored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **✅ Hackerato con successo il database**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])


@client.createCommand(
    command=("tr [Messaggio]", plugin_category),
    outgoing=True, regex=r"tr(?: |$|\n)([\s\S]*)"
)
async def translate(event: NewMessage.Event) -> None:
    translator = Translator()
    if event.reply_to_msg_id:
        r_message = await event.get_reply_message()
        text = r_message.message
    else:
        text = event.matches[0].group(1)
        if not text:
            await event.edit(f"`Traduci un messaggio`")
            return
    await event.edit(f"`Sto traducendo..`")
    translated = translator.translate(text, dest='it')
    if translated.src != 'it':
        try:
            after_tr_text = translated.text
            output_str = f"**Traduzione:**\n{after_tr_text}"
            await event.edit(output_str)
        except Exception as exc:
            await event.edit(f"Errore\n `{str(exc)}`")
    else:
        await event.edit(f"`Questo testo è già in italiano..`")


@client.createCommand(
    command=("ph", plugin_category),
    outgoing=True, regex=r"ph(?: |$|\n)([\s\S]*)"
)
async def ph(event: NewMessage.Event) -> None:
    await event.edit(
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣧⣤⣤⠀⢠⣤⡄⢸⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿   ⠸⠿⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣿⣿⠿⠷⣤⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⡏⢀⣤⣤⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⡇⠘⠿⠿⠃⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⡿⠦⠤⠤⠴⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣧⣤⣤⣄⡀   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⡀   ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠉⠉⢉⣉⣉⣉⣉⣉⣉⡉⠉⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⠻⠿⠿⠿⣿⡿⠿⠇⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⣤⣤⣤⣤⣾⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⢉⣩⣭⣭⣭⡄⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⣿⡟⠋⠉⠋⠁⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⣾⣿⣶⣶⣶⡆⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⣶⣶⣶⣶⣶⣶⣶⡆⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⣾⣏⠀⠀⣹⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⠀⠀⠘⠿⠿⠿⠟⠃⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿\n"
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n")


@client.createCommand(
    command=("tspam [Messaggio]", plugin_category),
    outgoing=True, regex=r"tspam(?: |$|\n)([\s\S]*)"
)
async def tspam(event: NewMessage.Event) -> None:
    tspam = event.matches[0].group(1)
    message = tspam.replace(" ", "")
    for letter in message:
        await event.respond(letter)
    await event.delete()


@client.createCommand(
    command=("timer [Tempo in minuti] [Messaggio]", plugin_category),
    outgoing=True, regex=r"timer(?: |$|\n)([\s\S]*)"
)
async def timer(event: NewMessage.Event) -> None:
    message = event.matches[0].group(1)
    text = message.split(" ")
    if message:
        try:
            if len(text[0]) >= 1:
                value = int(text[0])
                await event.delete()
                await asyncio.sleep(value * 60)
                arg = message.partition(text[0])[2]
                await event.respond(arg)
            else:
                await event.edit("**❗️ Devi inserire il messaggio!**")
        except ValueError:
            await event.edit('__Devi inserire un tempo in minuti valido!__')
    else:
        await event.edit('**❗️ Utilizzo corretto:** `.timer [Tempo in minuti] [Messaggio]`')
