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
