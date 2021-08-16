
import re
import logging
from typing import Tuple, Union

from telethon.tl import types

from ..utils.events import command


LOGGER = logging.getLogger(__name__)


async def get_user_from_msg(event: command.Event) -> Union[int, str, None]:
    user = None
    match = event.matches[0].group(1)

    if match == "this":
        match = str(event.chat.id)

    if event.entities:
        for entity in event.entities:
            if isinstance(entity, types.MessageEntityMentionName):
                return entity.user_id
            elif isinstance(entity, types.MessageEntityMention):
                offset = entity.offset
                length = entity.length
                maxlen = offset + length
                return event.text[offset:maxlen]

    if match:
        if isinstance(match, str) and match.isdigit():
            user = int(match.strip())
        else:
            user = match.strip()

    return user


async def get_entity_from_msg(event: command.Event) -> Tuple[
    Union[None, types.User], Union[None, bool, str], Union[None, bool, str]
]:
    exception = False
    entity = None
    match = event.matches[0].group(1)

    pattern = re.compile(r"(@?\w+|\d+)(?: |$)(.*)")
    user = pattern.match(match).group(1) if match else None
    extra = pattern.match(match).group(2) if match else None
    reply = await event.get_reply_message()

    if reply and not (user and extra):
        user = reply.from_id
        extra = match.strip()

    user = int(user) if isinstance(user, str) and user.isdigit() else user
    if not user:
        return None, None, "Couldn't fetch an entity from your message!"

    try:
        entity = await event.client.get_entity(user)
    except Exception as e:
        exception = True
        LOGGER.exception(e)

    return entity, extra, exception
