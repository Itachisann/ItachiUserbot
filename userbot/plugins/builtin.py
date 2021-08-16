
import datetime
import io
import logging
import os
import sys

from userbot import client
from userbot.core.events import command
from userbot.core.helpers import restart


@client.createCommand(
    command=('ping', 'www'),
    outgoing=True, regex='ping$', builtin=True
)
async def ping(event: command.Event) -> None:
    start = datetime.datetime.now()
    await event.answer("**Ping**")
    duration = (datetime.datetime.now() - start)
    milliseconds = duration.microseconds / 1000
    await event.answer(f"**Ping:** `{milliseconds}ms`")


@client.createCommand(
    command=("restart", 'misc'),
    outgoing=True, regex='restart$', builtin=True
)
async def restarter(event: command.Event) -> None:
    await restart(event)


