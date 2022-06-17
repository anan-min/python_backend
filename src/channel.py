"""Functions relating to channel - Iteration 1"""
from src.error import AccessError, InputError
from src.utils import load_data, save_data, token_to_id

from src.helper_channel import channel_search, user_search
from src.helper_notification import added_notification_ch

def channel_invite_v2(token, channel_id, u_id):
    """Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately."""

    auth_user_id = token_to_id(token)
    if not type(channel_id) == int:
        channel_id = channel_id['channel_id']

    # Raise InputError if auth_user_id == u_id
    if int(auth_user_id) == int(u_id):
        raise InputError

    # Raise InputError when u_id refers to invalid user.
    if user_search(u_id) is InputError:
        raise InputError

    # Raise InputError if invalid channel
    if channel_search(token, channel_id, 0) is InputError:
        raise InputError

    data = load_data()
    auth_user_data = data["users"][str(auth_user_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        auth_user_data.pop(i)

    # u_id is not currently channel_member
    if not auth_user_data in data["channel_info"][str(channel_id)]["all_members"]:
        raise AccessError

    # Raise AccessError when authorised user is not already a member of channel.
    valid_channel = channel_search(token, channel_id, 1)
    if valid_channel in (InputError, AccessError):
        raise valid_channel


    # Add user to channel.
    user_data = data["users"][str(u_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        user_data.pop(i)
    data["channel_info"][str(channel_id)]["all_members"].append(user_data)
    data["channels"]["channels"][str(channel_id)]["all_members"].append(user_data)
    save_data(data)

    # Send notification to added user
    added_notification_ch(token, channel_id, u_id)

    return {
    }

def channel_details_v2(token, channel_id):
    """Given a channel_id that the authorised user
    is part of, provide basic details about the channel"""

    if not type(channel_id) == int:
        channel_id = channel_id['channel_id']


    # Saves return value of channel_search (True, AccessError, InputError)
    search_return_value = channel_search(token, channel_id, 1)
    if search_return_value in (InputError, AccessError):
        raise search_return_value

    data = load_data()
    return data["channel_info"][str(channel_id)]

def channel_messages_v2(token, channel_id, start):
    """Given a Channel with ID channel_id that the
    authorised user is part of, return up to 50 messages."""

    if not type(channel_id) == int:
        channel_id = channel_id['channel_id']


    # Saves return value of channel_search (True, AccessError, InputError)
    search_return_value = channel_search(token, channel_id, 1)
    if search_return_value in (AccessError, InputError):
        raise search_return_value

    data = load_data()
    if data["messages"]["total"] == 0:
        raise InputError
    elif str(channel_id) not in data["messages"]:
        raise InputError
    else:
        total = len(data["messages"][str(channel_id)]["messages"])

    if start > total:
        raise InputError

    return_messages = {}

    # user request reaches end of message history
    if start + 50 > total:
        return_messages["messages"] = data["messages"][str(channel_id)]["messages"][start:total]
        return_messages["start"] = start
        return_messages["end"] = -1
        return return_messages

    # standard user message request
    return_messages["messages"] = data["messages"][str(channel_id)]["messages"][start:start+50]
    return_messages["start"] = start
    return_messages["end"] = start + 50
    return return_messages



def channel_leave_v1(token, channel_id):
    """Given a channel_id of a channel that the
    authorised user is part of, removes them from that channel."""


    auth_user_id = token_to_id(token)
    if not type(channel_id) == int:
        channel_id = channel_id['channel_id']

    # Raise InputError if channel_id is not valid channel.
    # Raise AccessError when channel_id refers to private channel.
    valid_channel = channel_search(token, channel_id, 3)
    if valid_channel in (InputError, AccessError):
        raise valid_channel

    # Remove user from channel
    data = load_data()
    user_data = data["users"][str(auth_user_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        user_data.pop(i)

    # u_id is not currently owner of channel
    if not user_data in data["channel_info"][str(channel_id)]["all_members"]:
        raise InputError

    data["channel_info"][str(channel_id)]["all_members"].remove(user_data)
    data["channels"]["channels"][str(channel_id)]["all_members"].remove(user_data)
    if valid_channel == 1:
        data["channel_info"][str(channel_id)]["owner_members"].remove(user_data)
        data["channels"]["channels"][str(channel_id)]["owner_members"].remove(user_data)
    save_data(data)

    return {
    }


def channel_join_v2(token, channel_id):
    """Given a channel_id of a channel that the
    authorised user can join, adds them to that channel."""

    auth_user_id = token_to_id(token)

    if not type(channel_id) == int:
        channel_id = channel_id['channel_id']

    # Raise InputError if channel_id is not valid channel.
    # Raise AccessError when channel_id refers to private channel.
    valid_channel = channel_search(token, channel_id, 2)
    if valid_channel in (InputError, AccessError):
        raise valid_channel

    # Add user to channel.
    data = load_data()
    user_data = data["users"][str(auth_user_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        user_data.pop(i)
    data["channel_info"][str(channel_id)]["all_members"].append(user_data)
    data["channels"]["channels"][str(channel_id)]["all_members"].append(user_data)
    save_data(data)

    return {
    }

def channel_addowner_v1(token, channel_id, u_id):
    """Given a channel_id of a channel that the
    auth_user has permissions for, adds u_id to that channel as an owner."""

    auth_user_id = token_to_id(token)

    # Raise InputError if channel_id is not valid channel.
    # Raise AccessError when channel_id refers to private channel.
    valid_channel = channel_search(token, channel_id, 3)
    if (valid_channel in (InputError, AccessError)) or auth_user_id == 0:
        raise valid_channel

    # Add user to channel.
    data = load_data()
    user_data = data["users"][str(u_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        user_data.pop(i)
    auth_user_data = data["users"][str(auth_user_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        auth_user_data.pop(i)

    # auth_user_id is not currently owner of channel
    if not auth_user_data in data["channel_info"][str(channel_id)]["owner_members"]:
        raise AccessError
    
    if user_data in data["channel_info"][str(channel_id)]["owner_members"]:
        raise InputError
    if not user_data in data["channel_info"][str(channel_id)]["all_members"]:
        data["channel_info"][str(channel_id)]["all_members"].append(user_data)
        data["channels"]["channels"][str(channel_id)]["all_members"].append(user_data)
    data["channel_info"][str(channel_id)]["owner_members"].append(user_data)
    data["channels"]["channels"][str(channel_id)]["owner_members"].append(user_data)

    save_data(data)

    return {
    }

def channel_removeowner_v1(token, channel_id, u_id):
    """Given a channel_id of a channel that the
    auth_user has permissions for, removes u_id from that channel as an owner."""

    auth_user_id = token_to_id(token)

    # Raise InputError if channel_id is not valid channel.
    # Raise AccessError when channel_id refers to private channel.
    valid_channel = channel_search(token, channel_id, 3)
    if (valid_channel in (InputError, AccessError)) or auth_user_id == 0:
        raise valid_channel

    # Remove user to channel.
    data = load_data()
    user_data = data["users"][str(u_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        user_data.pop(i)
    auth_user_data = data["users"][str(auth_user_id)].copy()
    for i in ("permission_id", "password", "session_ids"):
        auth_user_data.pop(i)
    # auth_user_id is not currently owner of channel
    if not auth_user_data in data["channel_info"][str(channel_id)]["owner_members"]:
        raise AccessError
    # u_id is not currently owner of channel
    if not user_data in data["channel_info"][str(channel_id)]["owner_members"]:
        raise InputError
    # u_id is currently the only owner
    if len(data["channel_info"][str(channel_id)]["owner_members"]) == 1:
        raise InputError
    data["channel_info"][str(channel_id)]["owner_members"].remove(user_data)
    data["channels"]["channels"][str(channel_id)]["owner_members"].remove(user_data)
    save_data(data)

    return {
    }
