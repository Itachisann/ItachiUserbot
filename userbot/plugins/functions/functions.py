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
