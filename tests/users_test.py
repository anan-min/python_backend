from src.users import users_all_v1, users_stats_v1
from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2
from src.message import message_send_v2
from src.dm import dm_create_v1
from src.channel import channel_join_v2
from datetime import date, datetime

def test_users_all_v1():
    clear_v1()
    user = auth_register_v2('alex@email.com', 'MyPassword', 'Alex', 'Culic')
    user2 = auth_register_v2('John@email.com', 'JohnsPassword', 'John', 'Doe')

    user_id1 = user['auth_user_id']
    user_id2 = user2['auth_user_id']
    expected_output = {}

    expected_output[f'{user_id1}'] = {
        'u_id': f'{user_id1}',
        'name_first': 'Alex',
        'name_last': 'Culic',
        'handle_str': 'alexculic',
        'email': 'alex@email.com'
    }
    expected_output[f'{user_id2}'] = {
        'u_id': f'{user_id2}',
        'name_first': 'John',
        'name_last': 'Doe',
        'handle_str': 'johndoe',
        'email': 'John@email.com'
    }

    assert users_all_v1(user['token']) == expected_output

def test_users_stats_none():
    clear_v1()

    time_stamp = datetime.now().strftime('%H:%M %d/%m/%Y')

    expected_output = {
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

    user1 = auth_register_v2('alex@email.com', 'password55', 'Alex', 'Culic')
    
    assert users_stats_v1(user1['token']) == expected_output


def test_users_stats():
    clear_v1()

    time_stamp = datetime.now().strftime('%H:%M %d/%m/%Y')

    
    expected_output = {
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


    user1 = auth_register_v2('alex@email.com', 'password55', 'Alex', 'Culic')
    user2 = auth_register_v2('camila@email.com', 'password33', 'Camila', 'Moro')
    user3 = auth_register_v2('zhitong@email.com', 'password11', 'Zhitong', 'Chen')
    user4 = auth_register_v2('anan@email.com', 'password55', 'Anan', 'Mit')

    channel1 = channels_create_v2(user1['token'], 'Alexs Channel', True)
    channel_join_v2(user2['token'], channel1)
    channel_join_v2(user3['token'], channel1)
    dm_create_v1(user1['token'], [user2['auth_user_id'], user3['auth_user_id']])
    message_send_v2(user1['token'], channel1, 'Hey')
    message_send_v2(user2['token'], channel1, 'Hi')
    message_send_v2(user3['token'], channel1, 'Whats up guys')
    dm_create_v1(user2['token'], user3['auth_user_id'])
    dm_create_v1(user4['token'], user1['auth_user_id'])

    expected_output['messages_exist'][0]['num_messages_exist'] = 3
    expected_output['channels_exist'][0]['num_channels_exist'] = 1
    expected_output['dms_exist'][0]['num_dms_exist'] = 3
    expected_output['utilization_rate'] = 0.75


    assert users_stats_v1(user1['token']) == expected_output

    for i in range(0, 5):
        for num in range(0, 20):
            message_send_v2(user1['token'], channel1, str(num)+str(i))

    expected_output['messages_exist'][0]['num_messages_exist'] += 100
    expected_output['utilization_rate'] = 0.75

    assert users_stats_v1(user1['token']) == expected_output

    auth_register_v2('toby@email.com', 'toby9912', 'Tobias', 'Wong')

    expected_output['utilization_rate'] = 0.6
    
    assert users_stats_v1(user1['token']) == expected_output
