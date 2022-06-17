from src.dm import dm_create_v1
from src.error import InputError
from src.user import user_profile_setemail_v2, user_profile_sethandle_v1, user_profile_setname_v2, user_profile_v2, user_profile_uploadphoto_v1, user_stats_v1
from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v2
from src.message import message_send_v2
from datetime import date, datetime
import pytest

def test_profile_v2():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'securepassw0rd11', 'Alex', 'Culic')
    auth_register_v2('john@email.com', 'Password55', 'John', 'Doe')
    test_output = {
            'u_id': user['auth_user_id'],         
            'name_first': 'Alex',
            'name_last': 'Culic',
            'handle_str': 'alexculic',
            'email': 'alex@email.com'
        }
    assert user_profile_v2(user['token'], user['auth_user_id']) == test_output

def test_profile_v2_not_found():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'securepassw0rd11', 'Alex', 'Culic')

    with pytest.raises(InputError):
        user_profile_v2(user['token'], 99)


def test_user_profile_setname_v2():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'securepassw0rd11', 'Alex', 'Culic')
    user_profile_setname_v2(user['token'], "John", "Doe")
    test_output = {
            'u_id': user['auth_user_id'],
            'name_first': 'John',
            'name_last': 'Doe',
            'handle_str': 'alexculic',
            'email': 'alex@email.com'
    }
    assert user_profile_v2(user['token'], user['auth_user_id']) == test_output

def test_user_profile_setname_v2_name_first_length():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_setname_v2(user['token'], 'x' * 51, 'x')

def test_user_profile_setname_v2_name_last_length():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_setname_v2(user['token'], 'x', 'x' * 51)

def test_user_profile_setname_v2_name_length():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_setname_v2(user['token'], 'x' * 51, 'x' * 51)

def test_user_setemail_v2():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'Password99', 'alex', 'culic')
    user_profile_setemail_v2(user['token'], 'email@email.com')
    test_output = {
            'u_id': user['auth_user_id'],
            'name_first': 'alex',
            'name_last': 'culic',
            'handle_str': 'alexculic',
            'email': 'email@email.com'
        }
    assert user_profile_v2(user['token'], user['auth_user_id']) == test_output


def test_user_setemail_v2_invalid():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_setemail_v2(user['token'], 'not an email')

def test_user_setemail_v2_taken():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    auth_register_v2('john@email.com', 'Password55', 'John', 'Doe')
    with pytest.raises(InputError):
        user_profile_setemail_v2(user['token'], 'john@email.com')

def test_user_sethandle_v2():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'Password99', 'Alex', 'Culic')
    token = user['token']
    user_profile_sethandle_v1(token, 'New Handle')
    test_output = {
            'u_id': user['auth_user_id'],
            'name_first': 'Alex',
            'name_last': 'Culic',
            'handle_str': 'New Handle',
            'email': 'alex@email.com'
        }
    assert user_profile_v2(user['token'], user['auth_user_id']) == test_output

def test_user_sethandle_v2_short():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user['token'], 'a')

def test_user_sethandle_v1_long():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user['token'], 'a' * 99)

def test_user_sethandle_v1_taken():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password99', 'Alex', 'Culic')
    auth_register_v2('john@email.com', 'password323', 'John', 'Doe')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user['token'], 'johndoe')

def test_user_setimg():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password55', 'Alex', 'Culic')
    assert(user_profile_uploadphoto_v1(user['token'], 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg', 0, 0, 480, 480)) == {}

def test_user_setimg_invalidurl():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password55', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user['token'], 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1', 0, 0, 480, 480)

def test_user_setimg_invalid_dimensions():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'password55', 'Alex', 'Culic')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user['token'], 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg', 0, 0, 480, 10000)
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(user['token'], 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg', -1, 0, 480, 480)

def test_user_stats_none():
    clear_v1()
    user1 = auth_register_v2('alex@gmail.com', 'password55', 'Alex', 'Culic')
    
    time_stamp = datetime.now().strftime('%H:%M %d/%m/%Y')

    expected_output = {
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

    assert user_stats_v1(user1['token']) == expected_output

def test_user_stats():
    clear_v1()
    user1 = auth_register_v2('alex@email.com', 'password55', 'Alex', 'Culic')
    user2 = auth_register_v2('anan@email.com', 'password22', 'Anan', 'M')

    channel1 = channels_create_v2(user1['token'], 'Alexs Channel', True)
    
    channel_join_v2(user2['token'], channel1)
    message_send_v2(user1['token'], channel1, 'Hello World')
    
    #User 1 has joined 1 channel and sent 1 message
    time_stamp = datetime.now().strftime('%H:%M %d/%m/%Y')
    expected_output = {
        'channels_joined': [{
            'num_channels_joined': 1,
            'time_stamp': time_stamp
        }],
        'dms_joined': [{
            'num_dms_joined': 0,
            'time_stamp': time_stamp
        }], 
        'messages_sent': [{
            'num_messages_sent': 1,
            'time_stamp': time_stamp
        }],
        'involvement_rate': 1.0
    }

    assert user_stats_v1(user1['token']) == expected_output

    #User 2 has joined 1 channel and sent 0 messages
    expected_output['messages_sent'][0]['num_messages_sent'], expected_output['involvement_rate'] = 0 , 0.5
    assert user_stats_v1(user2['token']) == expected_output

    channel2 = channels_create_v2(user2['token'], 'User2 Channel', True)
    
    #User 2 has joined 2 channels
    expected_output['channels_joined'][0]['num_channels_joined'] = 2
    expected_output['involvement_rate'] = 0.67
    assert user_stats_v1(user2['token']) == expected_output

    channel_join_v2(user1['token'], channel2)
    message_send_v2(user1['token'], channel2, 'Hello again!')

    #User 1 has joined 2 channels and sent a message in each channel
    expected_output['messages_sent'][0]['num_messages_sent'] = 2
    expected_output['involvement_rate'] = 1
    
    assert user_stats_v1(user1['token']) == expected_output

    dm_create_v1(user1['token'], user2['auth_user_id'])
    
    #User 1 has created a dm with user2
    expected_output['dms_joined'][0]['num_dms_joined'] = 1
    
    assert user_stats_v1(user1['token']) == expected_output

    #User 2 has joined 2 channels and 1 dm and sent 0 messages
    expected_output['messages_sent'][0]['num_messages_sent'], expected_output['involvement_rate'] = 0, 0.6

    assert user_stats_v1(user2['token']) == expected_output



    