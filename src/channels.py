"""Importing functions"""
from src.data import users, channel_info, channels, channel_standup
from src.error import InputError, AccessError
from src.utils import load_data, save_data, token_to_id


def channels_list_v2(token):
    """

    :param token:
    :return:
    """

    """Given a valid user id, returns a list of all channels the user is a member of"""
    
    data = load_data()
    u_id = token_to_id(token)
    all_users = data["users"]
    all_channels = data["channels"]
    info_channel = data["channel_info"]
    
    # IF USERID NOT FOUND IN USER DICTIONARY RAISE ERROR
    if u_id not in all_users:
        raise AccessError()

    if "channels" not in all_channels:
        return {
            "channels": [],
        }

    # provide list of all channel that user is part of
    channels_list = []
    for channel_id, channelinfo in info_channel.items():
        members = channelinfo["all_members"]
        i = 0
        while i < len(members): 
            if int(u_id) == members[i]['u_id']:
                channel_detail = {
                    "channel_id": int(channel_id),
                    "name": channelinfo["name"],
                }
                channels_list.append(channel_detail)
            i += 1

    save_data(data)
    return {'channels': channels_list}

def channels_listall_v2(token):
    """

    :param token:
    :return channels: 
    """
    data = load_data()
    u_id = token_to_id(token)
    users_all = data['users']
    all_channels = data['channels']
    info_channel = data["channel_info"]

    if u_id not in users_all:
        raise AccessError()

    if "channels" not in all_channels:
        return {
            "channels": [],
        }

    channels_list = []

    
    for channel_id, channelinfo in info_channel.items():
        channel_detail = {
            "channel_id": int(channel_id),
            "name": channelinfo["name"],
        }
        channels_list.append(channel_detail)

    save_data(data)
    return {
        "channels": channels_list,
    }


    # return ['channels':channels['channels']]


def channels_create_v2(token, name, is_public):
    """

    :param token:
    :param name:
    :param is_public:
    :return:
    """
    """Given a valid user id creates a new channels"""

    data = load_data()
    userid = token_to_id(token)
    user_data = data["users"][userid]
    users_all = data['users']
    all_channels = data['channels']
    info_channel = data['channel_info']
    chmsgs = data["messages"]

    ## IF USER NOT FOUND RAISE ERROR
    if userid not in users_all:
        raise AccessError

    ## IF CHANNEL NAME LESS THAN 20 CHAR
    if len(name) > 20:
        raise InputError
    else:
    
        # Generating new channel ID
        if len(all_channels) < 1:
            channelid = 1
        else:
            channelid = 1 + len(all_channels['channels'])

        ## ASSIGN CHANNEL INFORMATION AND USER DETAILS TO CHANNEL
        newchannel = {
                        'name': name,
                        'owner_members': [
                                            {
                                                'u_id': user_data['u_id'],
                                                'email': user_data['email'],
                                                'name_first': user_data['name_first'],
                                                'name_last': user_data['name_last'],
                                                'handle_str': user_data['handle_str']
                                            }
                                        ],
                        'all_members' : [
                                            {
                                                'u_id': user_data['u_id'],
                                                'email': user_data['email'],
                                                'name_first': user_data['name_first'],
                                                'name_last': user_data['name_last'],
                                                'handle_str': user_data['handle_str']
                                            }
                                        ]
                    }
        info_channel[str(channelid)] = newchannel
        if not all_channels:
            all_channels['channels'] = {channelid: {
                                        "channel_id" : channelid,
                                        "name" : name,
                                        "is_public" : is_public,
                                        "owner_members" : newchannel['owner_members'],
                                        "all_members": newchannel['all_members']
                                        }
                                    }
        else:
            all_channels['channels'][channelid] = {
                                        "channel_id" : channelid,
                                        "name" : name,
                                        "is_public" : is_public,
                                        "owner_members" : newchannel['owner_members'],
                                        "all_members": newchannel['all_members']
                                    }

        chmsgs[str(channelid)] = {"messages":[]}

        data["channel_standup"][channelid] = {
                "is_active": False,
                "time_finish": "None",
                "length": 0,
                "buffered_list": []
        }

        
        save_data(data)
        return {'channel_id': channelid}



