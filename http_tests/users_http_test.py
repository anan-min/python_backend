import pytest
import requests
from datetime import datetime
from src.other import clear_v1


url = "http://127.0.0.1:8080/"


def test_users_all_test():
    clear_v1()

    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic"
    })

    payload = r.json()
    token = payload['token']

    r = requests.get(f'{url}/users/all/v1', json={
        'token':token
    })

    payload = r.json

    assert payload != {}

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

    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'alex@email.com',
        'password': 'password33',
        'name_first': 'Alex',
        'name_last': 'Culic'
    })

    token = r.json()['token']

    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'camila@email.com',
        'password': 'password333',
        'name_first': 'Alex',
        'name_last': 'Culic'
    })

    u2_id = r.json()['auth_user_id']

    #Create channel
    r = requests.post(f'{url}/channels/create/v2', json={
        'token': token,
        'name': 'Alexs Channel',
        'is_public': True
    })
    channel = r.json()['channel_id']
    expected_output['channels_exist'][0]['num_channels_exist'] += 1

    #Send Message
    r = requests.post(f'{url}/message/send/v2', json={
        'token': token,
        'channel_id': channel,
        'message': 'Hi'
    })
    expected_output['messages_exist'][0]['num_messages_exist'] += 1

    #Create DM
    r = requests.post(f'{url}/dm/create/v1', json={
        'token': token,
        'u_ids': u2_id
    })
    expected_output['dms_exist'][0]['num_dms_exist'] += 1
    

    r = requests.get(f'{url}/users/stats/v1', json={
        'token': token
    })
    payload = r.json()

    expected_output['utilization_rate'] = 0.5

    assert payload == expected_output