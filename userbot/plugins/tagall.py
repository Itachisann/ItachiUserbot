from userbot import client
from userbot.utils.events import command
from telethon.utils import get_display_name
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from urllib.parse import quote_plus
import asyncio
import os
from re import findall
plugin_category = 'tagall'

@client.createCommand(
    command=("tagall", plugin_category),
    outgoing=True,regex=r"tagall(?: |$)(.*)"
)
async def tagall(event: command.Event) -> None:
    if event.is_group or event.is_channel:
        await event.delete()
        if event.fwd_from:
            return
        mentions = "__Ho taggato tutti__"
        chat = await event.get_input_chat()
        async for x in event.client.iter_participants(chat, 100):
            mentions += f"[\u2063](tg://user?id={x.id})"
        await event.answer(mentions, reply=True)
