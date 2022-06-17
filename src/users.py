from src.error import InputError
from src.user import user_profile_v2
from src.utils import load_data
from src.utils import token_to_id
from datetime import date, datetime

def users_all_v1(token):
    """
    Returns a list of all users and their associated details

    Arguments:
        <token> - Session token of requesting user
    
    Return value:
        Dictionary containing profile information of all users

    """

    #Load data and initialize variables
    data = load_data()
    users = data['users']

    user_keys = users.keys()

    #Create empty dictionary
    all_users = {}

    #Iterate through u_id in users and add profile view to all_users dictionary
    for user in user_keys:
        all_users[user] = user_profile_v2(token, user)
    
    #Return populated dictionary
    return all_users

def users_stats_v1(token):
    
    time_stamp = datetime.now().strftime('%H:%M %d/%m/%Y')

    dreams_stats = {
        'channels_exist':[{
            'num_channels_exist': 0,
            'time_stamp': time_stamp
        }],
        'dms_exist':[{
            'num_dms_exist': 0,
            'time_stamp': time_stamp
        }],
        'messages_exist': [{
            'num_messages_exist': 0,
            'time_stamp': time_stamp
        }],
        'utilization_rate': 0
    }

    total_members = 0    
    total_active_members = 0
    data = load_data()

    users = data['users']
    dms = data['dms']

    for key in users.keys():    
        active = False
        total_members += 1
        if data['channels'] != {}:
            channels = data['channels']['channels']
            for channel_key in channels.keys(): #Access specific channel
                for item in channels[channel_key]['all_members']:
                    if item['u_id'] == int(key):
                        active = True

        if dms != {}:        
            for dm in dms.keys():
                dm_members = dms[dm]['members']['members']
                for member in dm_members:
                    if member == key:
                        active == True

        if active == True:
            total_active_members += 1



    if data['channels'] != {}:
        channels = data['channels']['channels']
        for key in channels.keys():
            dreams_stats['channels_exist'][0]['num_channels_exist'] += 1

        
    channel_messages = data['messages'].copy()
    channel_messages.pop('total')
    for key in channel_messages.keys():
        messages = channel_messages[key]
        for message_key in messages.keys():
            message = messages[message_key]
            dreams_stats['messages_exist'][0]['num_messages_exist'] += len(message)
    
    for key in dms.keys():
        dreams_stats['dms_exist'][0]['num_dms_exist'] += 1
    
    total_channels = dreams_stats['channels_exist'][0]['num_channels_exist']
    utilization_rate = dreams_stats['utilization_rate']

    if total_members != 0 and total_channels != 0:
        utilization_rate =  round(total_active_members/total_members, 2)
    else:
        utilization_rate = 0
    
    if utilization_rate > 1:
        utilization_rate = 1

    dreams_stats['utilization_rate'] = utilization_rate
    
    return dreams_stats