"""Importing functions"""

from src.channels import channels_list_v2
from src.dm import dm_list_v1
from src.helper_message import delete_user_messages
from src.error import InputError, AccessError
from src.utils import load_data, save_data, token_to_id

def admin_user_remove_v1(token,uid):
    '''
    :param token:
    :param uid:
    :return:
    '''
    """Removing user from dreams"""
    data = load_data()
    tokenuid = token_to_id(token)

    if not str(uid) in data["users"]:
        raise InputError

    if data["users"][tokenuid]["permission_id"] == 2:
        raise AccessError
    elif uid in data["users"]:
        if data["users"][uid]["permission_id"] == 2:
            raise InputError

    #Couting number of owners
    owners = 0
    for userdata in data["users"].values():
        if userdata["permission_id"] == 1: 
            owners += 1

    #Raising Input error if uid is only owner
    if data["users"][str(uid)]["permission_id"] == 1 and owners == 1:
        raise InputError

    #Removing user info
    data["users"][str(uid)]["name_first"] = "Removed"
    data["users"][str(uid)]["name_last"] = "user"
    data["users"][str(uid)]["email"] = "removed email"
    data["users"][str(uid)]["permission_id"] = 2

    delete_user_messages(uid)

    save_data(data)

    return {}

def admin_user_permission_change_v1(token, uid, permission_id):
    '''
    :param token:
    :param uid:
    :param permission_id:
    :return:
    
    Changing permission of uid user to permission specified by permission_id

    '''
    data = load_data()
    u_id = token_to_id(token)

    if str(uid) in data["users"]:
        if data["users"][str(u_id)]["permission_id"] == 2:
            raise AccessError
        elif permission_id != 2:
            if permission_id != 1:
                raise InputError

        data["users"][str(uid)]["permission_id"] = permission_id
        save_data(data)
    else:
        raise InputError
    
    return {}
