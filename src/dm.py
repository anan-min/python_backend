from src.utils import load_data, save_data, token_to_id
from src.error import InputError, AccessError
from src.helper_notification import added_notification_dm
import re


def dm_create_v1(token, u_ids):
    """

    :param token:
    :param u_ids:
    :return:

    """
    data = load_data()

    creator_id = token_to_id(token)
    if type(u_ids) == int:
        u_ids = [u_ids]
    u_ids.append(creator_id)

    users = data["users"]


    for u_id in u_ids:
        if f'{u_id}' not in users.keys():
            raise AccessError()

    name = generate_dm_name(creator_id, u_ids)

    members = {
        "owner": creator_id,
        "members": []
    }

    for u_id in u_ids:
        members['members'].append(f'{u_id}')
    
    dm_id = 1000
    while f"{dm_id}" in data["dms"]:
        dm_id += 1

    dm = {
        "dm_id": int(dm_id),
        "name": name,
        "owner": creator_id,
        "members": members,
        "u_ids": members['members']
    }
    data["dm_messages"][dm_id] = {"messages": []}
    data["dms"][dm_id] = dm
    save_data(data)


    [added_notification_dm(token, int(dm_id), i) for i in u_ids if not i == creator_id]

    return {
        "dm_id": dm_id,
        "name": name,
    }


def dm_list_v1(token):
    """

    :param token:
    :return:
    """
    data = load_data()

    u_id = token_to_id(token)

    dms = []
    for dm_id in data["dms"]:
        if is_member(u_id, dm_id):
            dms.append({
                "dm_id": f'{dm_id}',
                "name": data["dms"][f'{dm_id}']["name"]
            })

    return {
        "dms": dms
    }


def dm_details_v1(token, dm_id):
    """

    :param token:
    :param dm_id:
    :return:
    """
    data = load_data()
    dm_id = str(dm_id)

    u_id = token_to_id(token)

    if dm_id not in data["dms"]:
        raise InputError

    if not is_member(u_id, dm_id):
        raise AccessError

    dm = data["dms"][dm_id]

    return {
        "name": dm["name"],
        "members": dm["members"]
    }


def dm_remove_v1(token, dm_id):
    """

    :param token:
    :param dm_id:
    :return:
    """
    data = load_data()

    u_id = token_to_id(token)
    dm_id = str(dm_id)
    dms = data["dms"]

    if dm_id not in dms:
        raise InputError

    if u_id != dms[dm_id]["owner"]:
        raise AccessError

    data["dms"].pop(dm_id)
    save_data(data)

    return{

    }


def dm_invite_v1(token, dm_id, u_id):
    """

    :param token:
    :param dm_id:
    :param u_id:
    :return:

    check dm_id
    check u_id is the valid user
    check if the u_id is owner
    add users to the dm_id

    """
    data = load_data()
        
    # dm_id does not refer to an existing dm.
    if f'{dm_id}' not in data["dms"]:
        raise InputError

    # u_id does not refer to a valid user.
    users = data["users"]
    if f'{u_id}' not in users:
        raise InputError

    # the authorised user is not already a member of the DM
    if not is_member(f'{token_to_id(token)}', dm_id):
        raise AccessError

    # invite user to the dm_id
    owner = data["dms"][str(dm_id)]["members"]["owner"]
    members = data["dms"][str(dm_id)]["members"]["members"]

    data["dms"][str(dm_id)]["members"]["members"].append(f'{u_id}')
    added_notification_dm(token, f'{dm_id}', f'{u_id}')
    data["dms"][str(dm_id)]["name"] = generate_dm_name(owner, members)
    data["dms"][str(dm_id)]["u_ids"].append(u_id)

    save_data(data)

    return {

    }


def dm_leave_v1(token, dm_id):
    """

    :param token:
    :param dm_id:
    :return:
    """
    data = load_data()

    # u_id that associated with token
    u_id = token_to_id(token)

    # dm_id is not a valid DM

    if str(dm_id) not in data["dms"]:
        raise InputError

    # Authorised user is not a member of DM with dm_id
    if is_member(u_id, f'{dm_id}') == False:
        raise AccessError

    data["dms"][f'{dm_id}']["members"]["members"].remove(f'{u_id}')
    data["dms"][f'{dm_id}']["u_ids"].remove(f'{u_id}')

    # user leave from the dm
    owner = data["dms"][str(dm_id)]["members"]["owner"]
    members = data["dms"][str(dm_id)]["members"]["members"]

    data["dms"][f'{dm_id}']["name"] = generate_dm_name(owner, members)

    save_data(data)

    return {

    }


def dm_messages_v1(token, dm_id, start):
    data = load_data()
    u_id = token_to_id(token)

    # DM ID is not a valid DM
    if str(dm_id) not in data["dms"]:
        raise InputError

    # Authorised user is not a member of DM with dm_id
    if not is_member(u_id, dm_id):
        raise AccessError

    # start is greater than the total number of messages in the channel
    if data["messages"]["total"] == 0:
        raise InputError
    elif str(dm_id) not in data["dm_messages"].keys():
        raise InputError
    else:
        total = len(data["dm_messages"][str(dm_id)]["messages"])

    if start > total:
        raise InputError

    return_messages = {}

    if total == 0:
        return_messages["messages"] = dict()
        return_messages["start"] = start
        return_messages["end"] = start
    elif start + 50 > total:
        return_messages["messages"] = data["dm_messages"][str(dm_id)]["messages"][start:total]
        return_messages["start"] = start
        return_messages["end"] = -1
        return return_messages
    else:
        # standard user message request
        return_messages["messages"] = data["dm_messages"][str(dm_id)]["messages"][start:start + 50]
        return_messages["start"] = start
        return_messages["end"] = start + 50
        return return_messages


def generate_dm_name(owner, members):
    """
    updata or generate name in dms[dm_id]

    :param :
    :return:
    """
    data = load_data()
    users = data["users"]
    handles = [users[f'{u_id}']["handle_str"] for u_id in members]
    handles = sorted(handles)
    dm_name = ", ".join(handles)
    return dm_name


def is_member(u_id, dm_id):
    data = load_data()
    members = data["dms"][f'{dm_id}']
    if f'{u_id}' == (members["owner"]) or f'{u_id}' in members["members"]["members"]:
        return True
    else:
        return False


