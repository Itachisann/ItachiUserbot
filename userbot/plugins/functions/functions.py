
from userbot.core.events import NewMessage


async def get_rights(
    event: NewMessage.Event,
    change_info: bool = False,
    post_messages: bool = False,
    edit_messages: bool = False,
    delete_messages: bool = False,
    ban_users: bool = False,
    invite_users: bool = False,
    pin_messages: bool = False,
    add_admins: bool = False
) -> bool:
    chat = await event.get_chat()
    if chat.creator:
        return True
    rights = {
        'change_info': change_info,
        'post_messages': post_messages,
        'edit_messages': edit_messages,
        'delete_messages': delete_messages,
        'ban_users': ban_users,
        'invite_users': invite_users,
        'pin_messages': pin_messages,
        'add_admins': add_admins
    }
    required_rights = []
    for right, required in rights.items():
        if required:
            required_rights.append(getattr(chat.admin_rights, right, False))

    return all(required_rights)
