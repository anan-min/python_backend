from json import load
from src.error import InputError
from src.utils import load_data, save_data, token_to_id
import urllib.request
from PIL import Image
from datetime import date, datetime
import re

def user_profile_v2(token, u_id):
    """
    For a valid user, returns information about their user_id, email, first name, last name, and handle

    Arguments:
        <token> - Session token of requesting user
        <u_id> - <int> - Profile id of profile to be viewed

    <Exceptions>
        <InputError> - u_id does not match any existing user.

    Return value:
        Dictionary containing u_id, name_first, name_last, email of profile matching <u_id>
    
    """


    #Load data and initialize variables
    data = load_data()
    users = data['users']
    user_keys = users.keys()
    
    #Check if u_id in users
    if not f'{u_id}' in user_keys:
        raise InputError()

    user_profile = {}

    #Create view of user profile
    user_profile['u_id'] = u_id
    user_profile['name_first'] = users[f'{u_id}']['name_first']
    user_profile['name_last'] = users[f'{u_id}']['name_last']
    user_profile['handle_str'] = users[f'{u_id}']['handle_str']
    user_profile['email'] = users[f'{u_id}']['email']

    return user_profile


def user_profile_setname_v2(token, name_first, name_last):   
    """
    Update the authorised user's first and last name

    Arguments:
        <token> - Session token of requesting user
        <name_first> - <str> - New first name2 user is requesting
        <name_last> - <str> - New last name user is requesting
    
    Exceptions:
        <InputError> name_first or name_last length < 1
        <InputError> name_first or name_last length > 50
    
    Return value:
        {}

    """

    #name_first and name_last parameter check
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError()

    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError()

    #Load data and initialize variables
    data = load_data()
    users = data['users']
    auth_user_id = token_to_id(token)

    #Change matching users name_first and name_last
    users[f'{auth_user_id}']['name_first'] = name_first
    users[f'{auth_user_id}']['name_last'] = name_last

    save_data(data)

    return {
    }


def user_profile_setemail_v2(token, email):
    """
    Update the authorised user's email address

    Arguments:
        <token> - Session token of requesting user
        <email> - <str> - New email user is requesting

    Exceptions:
        <InputError> - <email> is not a valid email address
        <InputError> - <email> belongs to another account

    Return value:
        {}

    """

    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    
    #Load data and initialize variables
    data = load_data()
    users = data['users']
    auth_user_id = token_to_id(token)

    userkeys = users.keys()

    #Iterate through keys in dictionary and check paramater matches constraints
    for key in userkeys:
        if users[key]['email'] == email:
            raise InputError('Email taken')
    
    if not re.search(regex, email):
        raise InputError('Invalid Email')
    else:
        users[f'{auth_user_id}']['email'] = email

    save_data(data)

    return {
    }


def user_profile_sethandle_v1(token, handle_str):
    """
    Update the authorised user's handle (i.e. display name)

    Arguments:
        <token> - Session token of requesting user
        <handle_str> - <str> - New handle user is requesting

    Exceptions:
        <InputError> - <handle_str> length < 1
        <InputError> - <handle_str> length > 50
        <InputError> - <handle_str> is being used by another user

    Return value:
        {}

    """

    #Load data and initalize variables
    data = load_data()
    users = data['users']
    auth_user_id = token_to_id(token)
    
    #Handle paramater check
    if len(handle_str) < 3 or len(handle_str) > 50:
        raise InputError()

    userkeys = users.keys()
    
    #Search for duplicates
    for key in userkeys:
        if users[key]['handle_str'] == handle_str:
            raise InputError()

    #If pass replace handle_str
    users[f'{auth_user_id}']['handle_str'] = handle_str
    
    save_data(data)

    return {
    }

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):

    """
    Input Error -- img url invalid 
    x,y not with in dimensions of specified img
    img is not jpg
    """
    #Establish file path for image to be saved
    u_id = token_to_id(token)
    file_path = '..\\static\\profile_photos\\{0}.jpg'.format(u_id)

    #Check url is valid image
    if img_url.endswith('jpg') or img_url.endswith('jpeg'):
        urllib.request.urlretrieve(img_url, file_path)
    else:
        raise InputError('Invalid image url.')


    #Open Saved image, crop and re-save
    image = Image.open(file_path)

    if x_start < 0 or x_end < 0 or y_start < 0 or y_end < 0:
        raise InputError('Please enter valid crop co-ordinates')

    image_dimensions = image.size
    if x_start > image_dimensions[1] or x_end > image_dimensions[1]:
        raise InputError('Please enter valid crop co-ordinates')
    elif y_start > image_dimensions[1] or y_end > image_dimensions[0]:
        raise InputError('Please enter valid crop co-ordinates')
    else:
        cropped_image = image.crop((x_start, y_start, x_end, y_end))
        cropped_image.save(file_path)

    return {}

def user_stats_v1(token):
    
    ##Define user stats and variables necessary for involvement rate calculation
    
    time_stamp = datetime.now().strftime( '%H:%M %d/%m/%Y')
    user_stats = {
        'channels_joined': [{
            'num_channels_joined': 0,
            'time_stamp': time_stamp
        }],
        'dms_joined': [{
            'num_dms_joined': 0,
            'time_stamp': time_stamp
        }], 
        'messages_sent': [{
            'num_messages_sent': 0,
            'time_stamp': time_stamp
        }],
        'involvement_rate': 0
    }
    total_msg = 0
    total_dms = 0
    total_channels = 0


    ##Load data
    
    u_id = token_to_id(token)
    data = load_data()


    ##Count channels
    
    if data['channels'] != {}:
        channels = data['channels']['channels']
        for key in channels.keys():
            channel_members = channels[key]['all_members']
            total_channels += 1
            for member in channel_members:
                if member['u_id'] == int(u_id):
                    user_stats['channels_joined'][0]['num_channels_joined'] += 1
    else:
        user_stats['channels_joined'][0]['num_channels_joined'] = 0

    ##Count Messages
    
    channel_messages = data['messages'].copy()
    channel_messages.pop('total')
    for key in channel_messages.keys():
        messages = channel_messages[key]
        for message_key in messages.keys():
            message = messages[message_key]
            for item in message:
                total_msg += 1
                if item['u_id'] == int(u_id):
                    user_stats['messages_sent'][0]['num_messages_sent'] += 1
    
    
    ##Count dms

    dms = data['dms']
    for key in dms.keys():
        total_dms += 1
        dm_members = dms[key]['u_ids']
        for member in dm_members:
            if member == u_id:
                user_stats['dms_joined'][0]['num_dms_joined'] += 1

    
    ##Calculate involvement rate ((user stat count) / (total stat count))
    if (total_channels + total_dms + total_msg) != 0:
        user_stats['involvement_rate'] = (user_stats['messages_sent'][0]['num_messages_sent'] + user_stats['dms_joined'][0]['num_dms_joined'] + user_stats['channels_joined'][0]['num_channels_joined']) / (total_channels + total_dms + total_msg)
        user_stats['involvement_rate'] = round(user_stats['involvement_rate'], 2)

    return user_stats

