from src.utils import load_data, save_data, token_to_id


def tagged_notification_dm(token, dm_id, msg_id):
    """
    token = of user that is sending message
    dm_id = dm_id
    msg_id = message_id
    """
    # find tagger data
    data = load_data()
    tagger_id = token_to_id(token)
    tagger_handle = data['users'][f"{tagger_id}"]['handle_str']

    # find message at msg_id
    message = ""
    dm_messages = data["dm_messages"][f"{dm_id}"]["messages"]
    for message_detail in dm_messages:
        if message_detail["message_id"] == msg_id:
            message = message_detail["message"]
            break

    # find user handles and dm_name
    u_ids = data["dms"][f"{dm_id}"]["members"]["members"]
    users_data = data["users"]
    user_handles = [users_data[f"{u_id}"]["handle_str"] for u_id in u_ids]
    dm_name = data["dms"][f"{dm_id}"]["name"]

    # notify user that get tagged
    for handle, u_id in zip(user_handles, u_ids):
        if f"@{handle}" in message:
            if data["users"][f"{tagger_id}"]["name_first"] == "Removed":
                event = {
                    "channel_id": -1,
                    "dm_id": dm_id,
                    "notification_message": "f{tagger_handle} tagged you in {dm_name}: Removed User"
                }
            else:
                event = {
                    "channel_id": -1,
                    "dm_id": dm_id,
                    "notification_message": f"{tagger_handle} tagged you in {dm_name}: {message[0:20]}"
                }
            if str(u_id) in data["notifications"].keys():
                data["notifications"][str(u_id)].insert(0, event)
            else:
                data["notifications"][str(u_id)] = [event]

    
    save_data(data)


def tagged_notification_ch(token, ch_id, msg_id):
    """
    token = of user that is sending message
    chid = channel_id
    msgid = message_id
    uid = auth_user_id of user being tagged
    """
    # retrieve tagger data
    data = load_data()
    tagger_id = token_to_id(token)
    tagger_handle = data['users'][f"{tagger_id}"]['handle_str']

    # retrieve channel data
    channel = data["channel_info"][f"{ch_id}"]
    channel_members = channel["all_members"]
    channel_name = channel["name"]

    # retrieve message at message_id
    message = ""
    channel_messages = data["messages"][f"{ch_id}"]["messages"]
    for message_detail in channel_messages:
        if message_detail["message_id"] == msg_id:
            message = message_detail["message"]

    # retrieve user data and handles
    users_data = data["users"]
    u_ids = [member["u_id"] for member in channel_members]
    user_handles ={uid : users_data[f"{uid}"]["handle_str"] for uid in u_ids}

    # notify user that is the tagged in channel message
    for uid, handle in user_handles.items():
        if f"@{handle}" in message:
            event = {
                "channel_id": ch_id,
                "dm_id": -1,
                "notification_message": f"{tagger_handle} tagged you in {channel_name}: {message[0:20]}"
            }
            if str(uid) in data["notifications"].keys():
                data["notifications"][str(uid)].insert(0, event)
            else:
                data["notifications"][str(uid)] = [event]

    save_data(data)


def added_notification_dm(token, dm_id, u_id):
    """
    token = of user that is adding another user to the dm
    dm_id = dm_id
    u_id = auth_user_id of user that is being added
    """
    # retrieve user data and dm_name
    data = load_data()
    auth_u_id = token_to_id(token)
    user_data = data["users"][auth_u_id]
    user_handle = user_data["handle_str"]
    dm_name = data["dms"][f"{dm_id}"]["name"]

    # notify user when added to dm
    event = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': f"{user_handle} added you to {dm_name}"
    }

    if str(u_id) in data["notifications"].keys():
        data["notifications"][str(u_id)].insert(0, event)
        save_data(data)

    else:
        data["notifications"][str(u_id)] = [event]
        save_data(data)


def added_notification_ch(token, ch_id, u_id):
    """
    token = of user that is adding another user to the dm
    chid = channel_id
    uid = auth_user_id of user that is being added
    """

    # retrieve owner data
    data = load_data()
    auth_u_id = token_to_id(token)
    user_data = data["users"][auth_u_id]
    user_handle = user_data["handle_str"]

    # retrieve channel_data
    channels_data = data["channels"]["channels"]
    channel_name = ""
    for channel in channels_data.values():
        if channel["channel_id"] == ch_id:
            channel_name = channel["name"]

    # notify user when added in channels
    event = {
        'channel_id': ch_id,
        'dm_id': -1,
        'notification_message': f"{user_handle} added you to {channel_name}"
    }

    if str(u_id) in data["notifications"].keys():
        data["notifications"][str(u_id)].insert(0, event)
        save_data(data)
    else:
        data["notifications"][str(u_id)] = [event]
        save_data(data)

def react_notification_ch(token, u_id, ch_id):
    # retrieve owner data
    data = load_data()
    reacterid = token_to_id(token)
    user_data = data["users"][reacterid]
    user_handle = user_data["handle_str"]

    # retrieve channel_data
    channels_data = data["channels"]["channels"]
    channel_name = ""
    for channel in channels_data.values():
        if channel["channel_id"] == int(ch_id):
            channel_name = channel["name"]

    # notify user when added in channels
    event = {
        'channel_id': int(ch_id),
        'dm_id': -1,
        'notification_message': f"{user_handle} reacted to your message in {channel_name}"
    }

    if str(u_id) in data["notifications"].keys():
        data["notifications"][str(u_id)].insert(0, event)
    else:
        data["notifications"][str(u_id)] = [event]
        
    save_data(data)

def react_notification_dm(token, dm_id, u_id):
    # retrieve user data and dm_name
    data = load_data()
    auth_u_id = token_to_id(token)
    user_data = data["users"][auth_u_id]
    user_handle = user_data["handle_str"]
    dm_name = data["dms"][f"{dm_id}"]["name"]

    # notify user when added to dm
    event = {
        'channel_id': -1,
        'dm_id': int(dm_id),
        'notification_message': f"{user_handle} reacted to your message in {dm_name}"
    }

    if str(u_id) in data["notifications"].keys():
        data["notifications"][str(u_id)].insert(0, event)

    else:
        data["notifications"][str(u_id)] = [event]
        
    save_data(data)
