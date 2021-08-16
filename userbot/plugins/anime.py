import json
import os
from urllib.request import urlopen

import requests
from userbot import client
from userbot.core.events import NewMessage

plugin_category = 'anime'


@client.createCommand(
    command=("waifu", plugin_category),
    outgoing=True, regex="(?:waifu|randomwaifu)(?: |$)(.+)?$"
)
async def animepic(event: NewMessage.Event) -> None:
    if event.fwd_from:
        return
    await event.answer("__Sto ottenendo la tua waifu...__")
    URL = urlopen("https://api.waifu.pics/sfw/waifu")
    data = json.loads(URL.read().decode())
    waifu = (data['url'])
    r = requests.get(waifu, allow_redirects=True)
    open('Waifu.jpg', 'wb').write(r.content)
    await event.delete()
    await event.respond("**Eheh..**", file='Waifu.jpg')
    os.system("rm -r Waifu.jpg")
