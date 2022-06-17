"""Functions relating to message - Iteration 2"""
from src.error import AccessError, InputError
from src.utils import load_data, save_data, token_to_id
from src.helper_channel import channel_search
from src.helper_message import message_author, find_message_text
from src.helper_notification import tagged_notification_ch, tagged_notification_dm, react_notification_ch, react_notification_dm
from src.dm import is_member
import time

def message_send_v2(token, channel_id, message_txt):
    """ Send a message from auth_user to channel_id """

    if not type(channel_id) == int:
        channel_id = channel_id["channel_id"]

    # Message length is > 1000
    if len(message_txt) > 1000:
        raise InputError

    # Finds auth_user_id
    auth_user_id = token_to_id(token)
    
    # Checks validity of channel
    valid_channel = channel_search(token, channel_id, 1)
    if valid_channel in (InputError, AccessError):
        raise valid_channel


    data = load_data()
    # First message sent in channel
    if not str(channel_id) in data["messages"].keys():
        data["messages"][str(channel_id)] = {"messages": []}

    # Adds message details to m_dict
    m_details = {}
    message_id = str(data["messages"]["total"])
    # message_id format ()
    message_id = int("1" + str(channel_id).zfill(3) + message_id)
    m_details["message_id"] = message_id
    data["messages"]["total"] += 1
    m_details["u_id"] = int(auth_user_id)
    m_details["message"] = message_txt
    m_details["time_created"] = round(time.time())
    m_details["is_pinned"] = False
    m_details["reacts"] = []

    # Appends message to message list in channel_id
    data["messages"][str(channel_id)]["messages"].append(m_details)
    save_data(data)

    # Sends notification of channel message
    tagged_notification_ch(token, channel_id, message_id)
    
    return {
        "message_id": message_id
    }


def message_senddm_v1(token, dm_id, message_txt):
    """ Send a message from auth_user to dm """
    
    # Message length is > 1000
    if len(message_txt) > 1000:
        raise InputError

    # Finds auth_user_id
    auth_user_id = token_to_id(token)
    
    data = load_data()

    # Checks validity of dmchannel
    if not str(dm_id) in data["dms"].keys():
        raise InputError

    if not str(auth_user_id) in data["users"].keys():
        raise AccessError

    # First message sent in channel
    if not str(dm_id) in data["dm_messages"].keys():
        data["dm_messages"][str(dm_id)] = {"messages": []}

    if not is_member(auth_user_id,dm_id):
        raise AccessError

    # Adds message details to m_dict
    m_details = {}
    message_id = str(data["messages"]["total"])
    # message_id format ()
    message_id = int("2" + str(dm_id).zfill(4) + message_id)
    m_details["message_id"] = message_id
    data["messages"]["total"] += 1
    m_details["u_id"] = int(auth_user_id)
    m_details["message"] = message_txt
    m_details["time_created"] = round(time.time())
    m_details["is_pinned"] = False
    m_details["reacts"] = []


    # Appends message to message list in channel_id
    data["dm_messages"][str(dm_id)]["messages"].append(m_details)
    save_data(data)

    # Sends notification of dm
    tagged_notification_dm(token, dm_id, message_id)

    return {
        "message_id": message_id
    }


def message_remove_v1(token, message_id):
    """ Given message_id, removes from channel_dm """

    auth_user_id = token_to_id(token)
    data = load_data()

    if not type(message_id) == int:
        message_id = message_id["message_id"]

    # Message id is channel message
    if str(message_id)[0] == "1":
        channel_id = int(str(message_id)[1:4])
        m_list = data["messages"][str(channel_id)]["messages"]
        author = message_author(auth_user_id, message_id, m_list)
        if author == None:
            raise InputError
        if not channel_search(token, channel_id, 14) or not author:
            raise AccessError
        
        deleted_list = [i for i in m_list if not i["message_id"] == message_id]
        data["messages"][str(channel_id)]["messages"] = deleted_list
        save_data(data)
        return {}

    elif str(message_id)[0] == "2":
        dm_id = int(str(message_id)[1:5])
        m_list = data["dm_messages"][str(dm_id)]["messages"]
        author = message_author(auth_user_id, message_id, m_list)
        if author == None:
            raise InputError
        if not channel_search(token, dm_id, 24) or not author:
            raise AccessError

        deleted_list = [i for i in m_list if not i["message_id"] == message_id]
        data["dm_messages"][str(dm_id)]["messages"] = deleted_list
        save_data(data)
        return {}

    raise InputError


def message_edit_v2(token, message_id, message):
    """ Given message, update message with new text """

    if not message:
        error_msg = message_remove_v1(token, message_id)
        if error_msg in (InputError, AccessError):
            return error_msg
        return {}

    if len(message) > 1000:
        raise InputError 

    auth_user_id = token_to_id(token)
    data = load_data()

    message_id = message_id["message_id"]

    # Message id is channel message
    if str(message_id)[0] == '1':
        channel_id = int(str(message_id)[1:4])
        m_list = data["messages"][str(channel_id)]["messages"]
        author = message_author(auth_user_id, message_id, m_list)
        if author == None:
            raise InputError
        if not channel_search(token, channel_id, 14) or not author:
            raise AccessError
        
        for m in data["messages"][str(channel_id)]["messages"]:
            if m["message_id"] == message_id:
                m.pop("message")
                m["message"] = message
                save_data(data)
                return {}

    elif str(message_id)[0] == '2':
        dm_id = int(str(message_id)[1:5])
        m_list = data["dm_messages"][str(dm_id)]["messages"]
        author = message_author(auth_user_id, message_id, m_list)
        if author == None:
            raise InputError
        if not channel_search(token, dm_id, 24) or not author:
            raise AccessError

        for m in data["dm_messages"][str(channel_id)]["messages"]:
            if m["message_id"] == message_id:
                if m["message_id"] == message_id:
                    m.pop("message")
                    m["message"] = message
                    save_data(data)
                    return {}

    raise InputError

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    """ Shares message to channel or dm """

    shared_message_id = 0

    # Sharing message to channel
    if not channel_id == -1:
        og_message = find_message_text(og_message_id)
        message += og_message
        if not type(channel_id) == int:
            channel_id = channel_id["channel_id"]
        shared_message_id = message_send_v2(token, channel_id, message)

    # Sharing message to dm
    if not dm_id == -1:
        og_message = find_message_text(og_message_id)
        message += og_message
        shared_message_id = message_senddm_v1(token, dm_id, message)
    
    # if shared_message_id in (InputError, AccessError):
    #     return class {shared_message_id}

    return {
        "shared_message_id": shared_message_id
    }

def message_pin_v1(token, message_id):
    "Pins message"
    # user id
    data = load_data()
    uid = int(token_to_id(token))
    chmsgs = data["messages"]
    dmmsgs = data["dm_messages"]
    info_ch = data["channel_info"]
    dms = data["dms"]

    found = False
    foundroute = 0
    for channel in info_ch.keys():
        i = 0
        while i < len(chmsgs[channel]["messages"]):
            if message_id == chmsgs[channel]["messages"][i]["message_id"]:
                if chmsgs[channel]["messages"][i]["is_pinned"] == True:
                    raise InputError
                found = True
                foundroute = chmsgs[channel]["messages"][i]
                j = 0
                isowner = False
                while j < len(info_ch[channel]["owner_members"]):
                    if uid == info_ch[channel]["owner_members"][j]["u_id"]:
                        isowner = True
                    j += 1
                if not isowner:
                    raise AccessError
            i += 1

    for dm in dmmsgs:
        i = 0
        while i < len(dmmsgs[(dm)]["messages"]):
            if message_id == dmmsgs[dm]["messages"][i]["message_id"]:
                if dmmsgs[dm]["messages"][i]["is_pinned"] == True:
                    raise InputError
                found = True
                foundroute = dmmsgs[dm]["messages"][i]
                if dms[dm]["owner"] != str(uid):
                    raise AccessError
            i += 1
    
    if not found:
        raise InputError

    foundroute["is_pinned"] = True
    save_data(data)
    return {}

def message_unpin_v1(token, message_id):
    "Pins message"
    # user id
    data = load_data()
    uid = int(token_to_id(token))
    chmsgs = data["messages"]
    dmmsgs = data["dm_messages"]
    info_ch = data["channel_info"]
    dms = data["dms"]

    found = False
    foundroute = 0
    for channel in info_ch:
        i = 0
        while i < len(chmsgs[channel]["messages"]):
            if message_id == chmsgs[channel]["messages"][i]["message_id"]:
                if chmsgs[channel]["messages"][i]["is_pinned"] == False:
                    raise InputError
                found = True
                foundroute = chmsgs[channel]["messages"][i]
                j = 0
                isowner = False
                while j < len(info_ch[channel]["owner_members"]):
                    if uid == info_ch[channel]["owner_members"][j]["u_id"]:
                        isowner = True
                    j += 1
                if not isowner:
                    raise AccessError
            i += 1

    for dm in dmmsgs:
        i = 0
        while i < len(dmmsgs[dm]["messages"]):
            if message_id == dmmsgs[dm]["messages"][i]["message_id"]:
                if dmmsgs[dm]["messages"][i]["is_pinned"] == False:
                    raise InputError
                found = True
                foundroute = dmmsgs[dm]["messages"][i]
                if dms[dm]["owner"] != str(uid):
                    raise AccessError
            i += 1
    
    if not found:
        raise InputError

    foundroute["is_pinned"] = False
    save_data(data)
    return {}

def message_sendlater_v1(token, channel_id, message, time_sent):
    """ Send a message from auth_user to channel_id """

    if not type(channel_id) == int:
        channel_id = channel_id["channel_id"]

    # Message length is > 1000
    if len(message) > 1000:
        raise InputError

    # Finds auth_user_id
    auth_user_id = token_to_id(token)
    
    # Checks validity of channel
    valid_channel = channel_search(token, channel_id, 1)
    if valid_channel in (InputError, AccessError):
        raise valid_channel

    # Checks if time_sent is greater than current time
    if time_sent < time.time():
        raise InputError

    data = load_data()
    # First message sent in channel
    if not str(channel_id) in data["messages"].keys():
        data["messages"][str(channel_id)] = {"messages": []}

    # Adds message details to m_dict
    m_details = {}
    message_id = str(data["messages"]["total"])
    # message_id format ()
    message_id = int("1" + str(channel_id).zfill(3) + message_id)
    m_details["message_id"] = message_id
    data["messages"]["total"] += 1
    m_details["u_id"] = int(auth_user_id)
    m_details["message"] = message
    m_details["time_created"] = round(time_sent)
    m_details["is_pinned"] = False

    def send():
        data = load_data()
        data["messages"][str(channel_id)]["messages"].append(m_details)
        save_data(data)
        tagged_notification_ch(token, channel_id, message_id)

    time.sleep(time_sent - round(time.time()))
    send()

    return {
        "message_id": message_id
    }

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    """ Send a message from auth_user to dm """
    
    # Message length is > 1000
    if len(message) > 1000:
        raise InputError

    # Finds auth_user_id
    auth_user_id = token_to_id(token)
    
    data = load_data()

    # Checks validity of dmchannel
    if not str(dm_id) in data["dms"].keys():
        raise InputError

    if not str(auth_user_id) in data["users"].keys():
        raise AccessError

    # Checks if time_sent is greater than current time
    if time_sent < time.time():
        raise InputError

    # First message sent in channel
    if not str(dm_id) in data["dm_messages"].keys():
        data["dm_messages"][str(dm_id)] = {"messages": []}

    if not is_member(auth_user_id,dm_id):
        raise AccessError

    # Adds message details to m_dict
    m_details = {}
    message_id = str(data["messages"]["total"])
    # message_id format ()
    message_id = int("2" + str(dm_id).zfill(4) + message_id)
    m_details["message_id"] = message_id
    data["messages"]["total"] += 1
    m_details["u_id"] = int(auth_user_id)
    m_details["message"] = message
    m_details["time_created"] = round(time.time())
    m_details["is_pinned"] = False

    def send():
        data = load_data()
        # Appends message to message list in channel_id
        data["dm_messages"][str(dm_id)]["messages"].append(m_details)
        save_data(data)
        # Sends notification of dm
        tagged_notification_dm(token, dm_id, message_id)

    time.sleep(time_sent - round(time.time()))
    send()

    return {
        "message_id": message_id
    }

def message_react_v1(token, message_id, react_id):
    ''' Reacts to message'''

    # if react id is not 1
    if int(react_id) != 1:
        raise InputError

    data = load_data()
    uid = int(token_to_id(token))
    chmsgs = data["messages"]
    dmmsgs = data["dm_messages"]
    info_ch = data["channel_info"]
    dms = data["dms"]

    found = False
    foundroute = 0
    senderid = 0
    ch_id = 0
    dm_id = 0
    for channel in info_ch:
        i = 0
        while i < len(chmsgs[channel]["messages"]):
            if message_id == chmsgs[channel]["messages"][i]["message_id"]:
                senderid = chmsgs[channel]["messages"][i]["u_id"]
                j = 0
                ismember = False
                while j < len(info_ch[channel]["all_members"]):
                    if uid == info_ch[channel]["all_members"][j]["u_id"]:
                        ismember = True
                    j += 1
                if not ismember:
                    raise AccessError
                if uid in chmsgs[channel]["messages"][i]["reacts"]:
                    raise InputError
                found = True
                foundroute = chmsgs[channel]["messages"][i]
                ch_id = int(channel)
                
            i += 1

    for dm in dmmsgs:
        i = 0
        while i < len(dmmsgs[dm]["messages"]):
            if message_id == dmmsgs[dm]["messages"][i]["message_id"]:
                if str(uid) not in dms[dm]["members"]["members"]:
                    raise AccessError
                if uid in dmmsgs[dm]["messages"][i]["reacts"]:
                    raise InputError
                found = True
                foundroute = dmmsgs[dm]["messages"][i]
                senderid = dmmsgs[dm]["messages"][i]["u_id"]
                dm_id = int(dm)
            i += 1
    
    if not found:
        raise InputError

    foundroute["reacts"].append(uid)

    if ch_id != 0:
        react_notification_ch(token, senderid, ch_id)
    elif dm_id != 0:
        react_notification_dm(token, dm_id, senderid)

    save_data(data)
    return {}
    
def message_unreact_v1(token, message_id, react_id):
    ''' Reacts to message'''

    # if react id is not 1
    if int(react_id) != 1:
        raise InputError

    data = load_data()
    uid = int(token_to_id(token))
    chmsgs = data["messages"]
    dmmsgs = data["dm_messages"]
    info_ch = data["channel_info"]
    dms = data["dms"]

    found = False
    foundroute = 0
    for channel in info_ch:
        i = 0
        while i < len(chmsgs[channel]["messages"]):
            if message_id == chmsgs[channel]["messages"][i]["message_id"]:
                j = 0
                ismember = False
                while j < len(info_ch[channel]["all_members"]):
                    if uid == info_ch[channel]["all_members"][j]["u_id"]:
                        ismember = True
                    j += 1
                if not ismember:
                    raise AccessError
                if uid not in chmsgs[channel]["messages"][i]["reacts"]:
                    raise InputError
                found = True
                foundroute = chmsgs[channel]["messages"][i]
                
            i += 1

    for dm in dmmsgs:
        i = 0
        while i < len(dmmsgs[dm]["messages"]):
            if message_id == dmmsgs[dm]["messages"][i]["message_id"]:
                if str(uid) not in dms[dm]["members"]["members"]:
                    raise AccessError
                if uid not in dmmsgs[dm]["messages"][i]["reacts"]:
                    raise InputError
                found = True
                foundroute = dmmsgs[dm]["messages"][i]
                
            i += 1
    
    if not found:
        raise InputError

    foundroute["reacts"].remove(uid)
    save_data(data)
    return {}
"""
def message_send_v2(token, channel_id, message):
    '''sends message in a channel'''
    data = load_data()
    uid = token_to_id(token)
    info_ch = data["channel_info"]
    ch_msgs = data["messages"]

    # input error when message is too long
    if len(message) > 1000:
        raise InputError
    
    j = 0
    ismember = False
    while j < len(info_ch[str(channel_id)]["all_members"]):
        if int(uid) == info_ch[str(channel_id)]["all_members"][j]["u_id"]:
            ismember = True
        j += 1
    if not ismember:
        raise AccessError
    # generating message id
    message_id = str(data["messages"]["total"])
    message_id = int("1" + str(channel_id).zfill(3) + message_id)
    data["messages"]["total"] += 1

    event = {
        "u_id" : int(uid),
        "message_id": message_id,
        "message": message,
        "time_created": round(time()),
        "is_pinned": False,
        "reacts": []
    }

    ch_msgs[str(channel_id)]["messages"].append(event)
    
    save_data(data)

    tagged_notification_ch(token, channel_id, message_id)

    return {"message_id": message_id}
    
"""
    
