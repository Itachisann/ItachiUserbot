
import datetime
import io
import logging
import os
import sys

from userbot import client, LOGGER, loggingHandler
from userbot.utils.events import NewMessage
from userbot.utils.helpers import restart


@client.onMessage(
    command=('ping', 'www'),
    outgoing=True, regex='ping$', builtin=True
)
async def ping(event: NewMessage.Event) -> None:
    start = datetime.datetime.now()
    await event.answer("**Ping**")
    duration = (datetime.datetime.now() - start)
    milliseconds = duration.microseconds / 1000
    await event.answer(f"**Ping:** `{milliseconds}ms`")


@client.onMessage(
    command=("restart", 'misc'),
    outgoing=True, regex='restart$', builtin=True
)
async def restarter(event: NewMessage.Event) -> None:
    await restart(event)


