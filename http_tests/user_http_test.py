import pytest
import requests
from datetime import datetime
from src.other import clear_v1

url = "http://127.0.0.1:8080/"

def test_profile_view():
    clear_v1()

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic"
    })

    payload = r.json()
    token = payload["token"]
    u_id = payload['auth_user_id']

    r = requests.get(f'{url}/user/profile/v2', json={
        'token': token,
        'u_id': u_id
    })

    payload = r.json()

    assert payload['name_first'] == 'Alex'


def test_setname():
    clear_v1()

    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic"
    })

    payload = r.json()
    token = payload['token']


    r = requests.put(f'{url}/user/profile/setname/v2',json={
        'token': token,
        "name_first": "John",
        "name_last": "Doe"
    })

    payload = r.json()

    assert payload == {}


def test_setemail():
    clear_v1()

    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic"
    })

    payload = r.json()
    token = payload["token"]

    r = requests.put(f'{url}/user/profile/setemail/v2', json={
        "token": token,
        "email": "john@email.com"
    })

    payload = r.json()

    assert payload == {}


def test_sethandle():
    clear_v1()

    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic" 
    })

    payload = r.json()
    token = payload["token"]
    
    r = requests.put(f'{url}/user/profile/sethandle/v1', json={
        "token": token,
        "handle_str": "newhandle"
    })

    payload = r.json()

    assert payload == {}

def test_users_all():
    clear_v1()

    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic"
    })

    payload = r.json()
    token = payload['token']

    r = requests.get(f'{url}/users/all/v2', json={
        'token': token
    })

    payload = r.json

    assert payload != {}

def test_user_stats():
    clear_v1()

    #Register User
    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "alex@email.com",
        "password": "mypassword99",
        "name_first": "Alex",
        "name_last": "Culic"
    })

    payload = r.json()
    token = payload['token']

    #Register 2nd user
    r = requests.post(f'{url}/auth/register/v2', json={
        "email": "anan@email.com",
        "password": "mypassword99",
        "name_first": "Anan",
        "name_last": "Mit"
    })

    payload = r.json()
    u2_id = payload['auth_user_id']
    
    #Create channel
    r = requests.post(f'{url}/channels/create/v2', json={
        "token": token,
        "name": "Alexs Channel",
        "is_public": True
    })

    payload = r.json()
    channel = payload['channel_id']

    #Send message on channel
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token,
        "channel_id": channel,
        "message": "Hello World!"
    })

    #Create dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token":token,
        "u_ids": u2_id
    })

    time_stamp = datetime.now().strftime('%H:%M %d/%m/%Y')
    expected_output = {
        'channels_joined': [{
            'num_channels_joined': 1,
            'time_stamp': time_stamp
        }],
        'dms_joined': [{
            'num_dms_joined': 1,
            'time_stamp': time_stamp
        }], 
        'messages_sent': [{
            'num_messages_sent': 1,
            'time_stamp': time_stamp
        }],
        'involvement_rate': 1.0
    }

    r = requests.get(f'{url}/user/stats/v1', json={
        'token':token
    })

    payload = r.json()

    assert payload == expected_output

def test_user_photo():
    clear_v1()
    
    r = requests.post(f'{url}/auth/register/v2', json={
        'email': 'alex@email.com',
        'password': 'password99',
        'name_first': 'Alex',
        'name_last': 'Culic'
    })

    payload = r.json()
    token = payload['token']

    r = requests.post(f'{url}/user/profile/uploadphoto/v1', json={
        'token': token, 
        'img_url': 'https://static.boredpanda.com/blog/wp-content/uploads/2020/05/700-1.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 480,
        'y_end': 480
    })

    payload = r.json()
    assert payload == {}