"""
Author: Zhitong Chen 
Date: 2021/4/16
Content: All funtion for standup 
"""
from src.error import AccessError, InputError
from src.utils import load_data, save_data, token_to_id
from src.helper_channel import channel_search
from threading import Timer
from datetime import timezone, datetime
from src.message import message_send_v2

def get_finish_time(length):
    now = datetime.now()

    year = now.year
    month = now. month
    date = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    dt = datetime(year, month, date, hour, minute, second)
    timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    time_finish = timestamp + length
    return {
        "time_finish": time_finish,
        "time_start": timestamp
    }

def standup_start_v1(token, channel_id, length):
    data = load_data()
    standup = data["channel_standup"]
    #check channel_id
    if channel_search(token, channel_id, 0) is InputError:
        raise InputError

    #check if user is in the channel
    if channel_search(token, channel_id, 1) is AccessError:
        raise AccessError

    #check is_active
    if standup[str(channel_id)]["is_active"] == True:
        raise InputError
    
    #begin standup
    standup[str(channel_id)]["is_active"] = True
    result = get_finish_time(length)
    standup[str(channel_id)]["time_finish"] = result["time_finish"]
    standup[str(channel_id)]["length"] = length
    save_data(data)

    time_curr = result["time_start"]
    while time_curr < result["time_finish"]:
        now = datetime.now()

        year = now.year
        month = now. month
        date = now.day
        hour = now.hour
        minute = now.minute
        second = now.second

        dt = datetime(year, month, date, hour, minute, second)
        time_curr = (dt - datetime(1970, 1, 1)).total_seconds()

        return {
            "time_finish": result["time_finish"]
        }

    #when time's up reset
    data = load_data()
    standup = data["channel_standup"]
    Timer(length, helper_standup_message, (token, channel_id, standup[str(channel_id)]["buffered_list"]))
    standup[str(channel_id)]["buffered_list"] = []
    standup[str(channel_id)]["length"] = 0
    standup[str(channel_id)]["is_active"] = False
    standup[str(channel_id)]["time_finish"] = "None"
    save_data(data)
    
    return {
        "time_finish": result["time_finish"]
    }

def standup_active_v1(token, channel_id):
    data = load_data()
    standup = data["channel_standup"]  

    #check channel_id
    if channel_search(token, channel_id, 0) is InputError:
        raise InputError


    if standup[str(channel_id)]["is_active"] == True:
        is_active = True
        time_finish = standup[str(channel_id)]["time_finish"]
    else:
        is_active = False
        time_finish = "None"
    return {
        "is_active": is_active,
        "time_finish": time_finish
    }

def standup_send_v1(token, channel_id, message):
    data = load_data()
    standup = data["channel_standup"]  
    buffered_list = []
    u_id = token_to_id(token)
    users = data["users"]

    if channel_search(token, channel_id, 0) is InputError:
        raise InputError

    #check if user is in the channel
    if channel_search(token, channel_id, 1) is AccessError:
        raise AccessError

    #check if message access 1000 character
    if len(message) > 1000:
        raise InputError

    for user in users:
        if u_id == user:
            username = users[u_id]["handle_str"]

    modified_message = username + ":"

    #check is_active
    if standup[str(channel_id)]["is_active"] == False:
        raise InputError
    
    #when all conditions fulfilled, add message to a buffered list and send them when the standup finished
    modified_message = modified_message + message
    buffered_list.append(modified_message)
    standup[str(channel_id)]["message"] = buffered_list
    save_data(data)
    return {}
     

def helper_standup_message(token, channel_id, buffered_list):
    data = load_data()
    auth_user_id = token_to_id(token)
    # First message sent in channel
    if not str(channel_id) in data["messages"].keys():
        data["messages"][str(channel_id)] = {"messages": []}

    #get the current time
    result = get_finish_time(10)
    time = result["time_start"]

    # Adds message details to m_dict
    m_details = {}
    message_id = str(data["messages"]["total"])
    
    # message_id format ()
    for message in buffered_list:
        message_id = int("1" + str(channel_id).zfill(3) + message_id)
        m_details["message_id"] = message_id
        data["messages"]["total"] += 1
        m_details["u_id"] = int(auth_user_id)
        m_details["message"] = message
        m_details["time_created"] = round(time)
        m_details["is_pinned"] = False

    # Appends message to message list in channel_id
    data["messages"][str(channel_id)]["messages"].append(m_details)
    save_data(data)
    


    

