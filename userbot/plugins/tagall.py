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
