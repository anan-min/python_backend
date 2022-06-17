"""Helper functions for channel.py"""
from src.channels import channels_listall_v2
from src.error import AccessError, InputError
from src.utils import load_data, token_to_id

def __str_or_int_match(search_term, search_type, l_dict):
    type_list = ["channel_id", "name", "is_public", "owner_members", "all_members"]
    
    # return dictionary in list containing channel info
    if search_type in range(2,5):
        for key in l_dict:
            for value in l_dict[key].values():
                if value[type_list[0]] == search_term:
                    return value[type_list[search_type]]

    # checks if search_term is in list_dictionary (channels)
    for key in l_dict:
        for value in l_dict[key].values():
            if value[type_list[search_type]] == search_term:
                return True
    return False

def __dm_str_or_int_match(search_term, search_type, l_dict):
    type_list = ["dm_id", "creator", "name", "members"]

    if search_type == 0:
        return str(search_term) in l_dict.keys()

    if search_type in range (1,4):
        for key in l_dict.values():
            if int(key[type_list[0]]) == int(search_term):
                if search_type == 3:
                    return key[type_list[search_type]]['members']
                return key[type_list[search_type]]

def user_channel_search(token, search_term, search_type):
    """Searches for specific search_term in search_type paramater"""
    l_dict = channels_listall_v2(token)

    auth_user_id = token_to_id(token)

    # checks if channel_id exists
    if search_type == 0:
        exists = 0

        for c in l_dict["channels"]:
            if c['channel_id'] == search_term:
                exists = 1
            
        if exists == 0:
            return InputError

    # checks if user is part of channel_id
    elif search_type == 1:
        if user_channel_search(token, search_term, 0) is True:
            # User is not part of channel_id
            # if not auth_user_id in channel_info[channel_id]["all_members"]:
            data = load_data()
            channels = data["channels"] 
            members = __str_or_int_match(search_term, 4, channels)
            status = False
            for user in members:
                if user["u_id"] == int(auth_user_id):
                    status = True
            if status == False:
                return AccessError
        # return InputError from invalid channel_id
        else:
            return InputError

    # checks if user is part of private channel
    elif search_type == 2:
        # Checks if channel_id exists
        if user_channel_search(token, search_term, 0) is not True:
            return InputError
        # Checks if channel is private
        data = load_data()
        channels = data["channels"]
        if not __str_or_int_match(search_term, search_type, channels):
            return AccessError

    # checks user"s permissions in channel
    elif search_type == 3:
        # Returns AccessError or InputError depending on if
        # user is part of channel and whether it exists
        error_msg = user_channel_search(token, search_term, 1)
        if error_msg in (AccessError, InputError):
            return error_msg
        # Checks owner list of channel to find u_id
        data = load_data()
        channels = data["channels"]
        value = __str_or_int_match(search_term, search_type, channels)
        for user in value:
            if user["u_id"] == auth_user_id:
                return 1
        return 2

    # checks channel message editing permissions
    elif search_type == 14:
        # auth_user is owner of Dreams
        if auth_user_id == 0:
            return True
        error_msg = user_channel_search(token, search_term, 3)
        if error_msg in (AccessError, InputError, 2):
            return error_msg

    # checks dm message editing permissions
    elif search_type == 24:
        data = load_data()
        # auth_user is owner of Dreams
        if auth_user_id == 0:
            return True
        l_dict = data["dms"]
        error_msg = __dm_str_or_int_match(search_term, 0, l_dict)
        if not error_msg:
            return False

        if str(auth_user_id) in __dm_str_or_int_match(search_term, 3, l_dict):
            return True
        
        return False
        # print(c_list)
        # for k in c_list:
        #     if c_list[k] == auth_user_id:
        #         return True 
        #     # if user["u_id"] == auth_user_id:
        #     #     return True
        # return False

    return True


def channel_search(token, search_term, search_type):
    """Outlines search parameters for user_channel_search"""
    # Primary function called in channel.py

    
    if not type(search_term) == int:
        search_term = search_term["channel_id"]


    # returns if channel_id exists for auth_user_id
    # search term is channel_id
    if search_type == 0:
        return user_channel_search(token, search_term, search_type)

    # returns if auth_user_id is in channel_id
    # search_term is channel_id
    if search_type == 1:
        return user_channel_search(token, search_term, search_type)

    # returns if channel is public
    # search_term is channel_id
    if search_type == 2:
        return user_channel_search(token, search_term, search_type)

    # returns user permissions (owner or member)
    if search_type == 3:
        return user_channel_search(token, search_term, search_type)

    # returns if user has permission to change channel message (author, owner of channel or owner of Dreams)
    # search term is channel or dm id
    if search_type == 14:
        return user_channel_search(token, search_term, search_type)

    # returns if user has permission to change channel message (author, owner of channel or owner of Dreams)
    # search term is channel or dm id
    if search_type == 24:
        return user_channel_search(token, search_term, search_type)

    # Should never occur as function is never called by user directly
    return "Invalid search_type"

def user_search(user_id):
    data = load_data()
    users = data["users"] 

    """Search for user_id in user dictionary"""
    if str(user_id) in users.keys():
        return users[str(user_id)]

    return InputError
