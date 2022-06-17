import pytest
import requests
import datetime, time
from src.other import clear_v1
from src.utils import load_data

url = "http://127.0.0.1:8080/"

def test_message_send_edit_messages_share_remove():
    clear_v1()

    # Create test user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "test1@gmail.com",
        "password": "password",
        "name_first": "first1",
        "name_last": "last1"
    })
    payload = r.json()
    token1 = payload["token"]

    # Create test channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "test_channel_1",
        "is_public": True
    })
    payload = r.json()
    channel_id_1 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "test_channel_2",
        "is_public": True
    })
    payload = r.json()
    channel_id_2 = payload["channel_id"]

    # User sends messages in channel 1
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token1,
        "channel_id": channel_id_1,
        "message": "hello world"
    })
    payload = r.json()
    message_id = payload["message_id"]

    # User edits message
    r = requests.put(f"{url}/message/edit/v2", json={
        "token": token1,
        "message_id": message_id,
        "message": "updated hello world!"
    })

    # Show messages in channel
    r = requests.get(f"{url}/channel/messages/v2", json={
        "token": token1,
        "channel_id": channel_id_1,
        "start": 0
    })

    # Share message in channel 1 to channel 2
    r = requests.post(f"{url}/message/share/v1", json={
        "token": token1,
        "og_message_id": message_id,
        "message": '',
        "channel_id": channel_id_2,
        "dm_id": -1
    })

    # Remove original message from channel 1
    r = requests.delete(f"{url}/message/remove/v1", json={
        "token": token1,
        "message_id": message_id
    })
    payload = r.json()
    assert payload == {}

def test_message_pin():
    clear_v1()
    # register 3 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]
    u_id2 = payload["auth_user_id"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "hillary@gmail.com",
        "password": "123456789",
        "name_first": "Hillary",
        "name_last": "Clinton"
    })
    payload = r.json()
    token3 = payload["token"]

    # user1 creates a channel, adds user2 and sends a message
    # create channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel1",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]
    # invites user2
    r = requests.post(f"{url}/channel/invite/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "u_id": u_id2
    })
    # sends channel message
    msg = "Welcome George"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()
    msg_id1 = payload["message_id"]

    # user1 creates dm with user2 and sends a message
    # creating dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token1,
        "u_ids": [u_id2]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]
    # dm message
    msg2 = "Hello George"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token1,
        "dm_id": dm_id1,
        "message": msg2
    })
    payload = r.json()
    msg_id2 = payload["message_id"]
    
    # trying to pin a msg with invalid msg id
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": 1234
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # pinning channel message and dm message
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # trying to pin messages which are already pinned
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # unpinning messages
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # user that is not part of channel or dm trying to pin
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token3,
        "message_id": msg_id1
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token3,
        "message_id": msg_id2
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # user that is not owner of channel or dm trying to pin
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token2,
        "message_id": msg_id1
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token2,
        "message_id": msg_id2
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # pinning channel message and dm message
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # success channels message
    r = requests.get(f"{url}/channel/messages/v2", json={
        "token": token2,
        "channel_id": channel_id1
    })
    payload = r.json()
    assert payload["messages"][0]["is_pinned"] == True
    
    # success dm message
    r = requests.get(f"{url}/dm/messages/v1", json={
        "token": token2,
        "channel_id": dm_id1
    })
    payload = r.json()
    assert payload["messages"][0]["is_pinned"] == True

def test_message_unpin():
    clear_v1()
    # register 3 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]
    u_id2 = payload["auth_user_id"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "hillary@gmail.com",
        "password": "123456789",
        "name_first": "Hillary",
        "name_last": "Clinton"
    })
    payload = r.json()
    token3 = payload["token"]

    # user1 creates a channel, adds user2 and sends a message
    # create channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel1",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # sends channel message
    msg = "Welcome George"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()
    msg_id1 = payload["message_id"]

    # user1 creates dm with user2 and sends a message
    # creating dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token1,
        "u_ids": [u_id2]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]
    # dm message
    msg2 = "Hello George"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token1,
        "dm_id": dm_id1,
        "message": msg2
    })
    payload = r.json()
    msg_id2 = payload["message_id"]
    
    # pinning channel message and dm message
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # trying to unpin a msg with invalid msg id
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": 1234
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # unpinning channel message and dm message
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # trying to unpin messages which are already unpinned
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # pinning messages
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/pin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # user that is not part of channel or dm trying to unpin
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token3,
        "message_id": msg_id1
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token3,
        "message_id": msg_id2
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # user that is not owner of channel or dm trying to unpin
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token2,
        "message_id": msg_id1
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token2,
        "message_id": msg_id2
    })
    payload = r.json()
    assert payload["name"] == "System Error" 

    # unpinning channel message and dm message
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id1
    })
    r = requests.post(f"{url}/message/unpin/v1", json={
        "token": token1,
        "message_id": msg_id2
    })

    # success channels message
    r = requests.get(f"{url}/channel/messages/v2", json={
        "token": token2,
        "channel_id": channel_id1
    })
    payload = r.json()
    assert payload["messages"][0]["is_pinned"] == False
    
    # success dm message
    r = requests.get(f"{url}/dm/messages/v1", json={
        "token": token2,
        "channel_id": dm_id1
    })
    payload = r.json()
    assert payload["messages"][0]["is_pinned"] == False

def test_message_and_dm_sendlater():
    clear_v1()

    # Create test users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "test1@gmail.com",
        "password": "password",
        "name_first": "first1",
        "name_last": "last1"
    })
    payload = r.json()
    token1 = payload["token"]
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "test2@gmail.com",
        "password": "password",
        "name_first": "first2",
        "name_last": "last2"
    })
    payload = r.json()
    user_id2 = payload["auth_user_id"]

    # Create test channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "test_channel_1",
        "is_public": True
    })
    payload = r.json()
    channel_id = payload["channel_id"]

    # Create dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token1,
        "u_ids": [user_id2]
    })
    payload = r.json()
    dm_id = payload["dm_id"]

    r = requests.post(f"{url}/messages/sendlater/v1", json={
        "token": token1,
        "channel_id": channel_id,
        "message": "hello",
        "time_sent": time.time() + 5
    })
    
    r = requests.post(f"{url}/messages/sendlaterdm/v1", json={
        "token": token1,
        "dm_id": dm_id,
        "message": "hello",
        "time_sent": time.time() + 5
    })


def test_message_react():
    clear_v1()
    # user1, user2 and user3 created
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]
    u_id1 = payload["auth_user_id"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]
    u_id2 = payload["auth_user_id"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "hillary@gmail.com",
        "password": "123456789",
        "name_first": "Hillary",
        "name_last": "Clinton"
    })
    payload = r.json()
    token3 = payload["token"]

    # user1 creates a channel, adds user2 and sends a message
    # create channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel1",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]
    # invites user2
    r = requests.post(f"{url}/channel/invite/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "u_id": u_id2
    })
    # sends channel message
    msg = "Welcome George"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()
    msg_id1 = payload["message_id"]

    # user1 creates dm with user2 and sends a message
    # creating dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token1,
        "u_ids": [u_id2]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]
    # dm message
    msg2 = "Hello George"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token1,
        "dm_id": dm_id1,
        "message": msg2
    })
    payload = r.json()
    msg_id2 = payload["message_id"]

    # input error with invalid messageid
    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": 1234,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    # input error with invalid react id
    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 5
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 5
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    # user 2 reacts
    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 1
    })

    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 1
    })

    # input error when user 2 tries to react again to same msg
    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    # user3 trying to react
    r = requests.post(f"{url}/message/react/v1", json={
        "token": token3,
        "message_id": msg_id1,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.post(f"{url}/message/react/v1", json={
        "token": token3,
        "message_id": msg_id2,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    data = load_data()
    expectedoutput = {'messages':
        [
            {
                "message_id": msg_id2,
                'u_id': u_id1,
                'message': msg2,
                'time_created':data["dm_messages"][str(dm_id1)]['messages'][0]['time_created'],
                'is_pinned': False,
                'reacts':[u_id2]
            },
            {
                "message_id": msg_id1,
                'u_id': u_id1,
                'message': msg,
                'time_created': data["messages"][str(channel_id1)]['messages'][0]['time_created'],
                'is_pinned': False,
                'reacts':[u_id2]
            }
        ]
    }
    r = requests.get(f"{url}/search/v2", json={
        "token": token1,
        "query_str": "George"
    })
    payload = r.json()
    assert expectedoutput == payload

def test_message_unreact():
    clear_v1()
    # user1, user2 and user3 created
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]
    u_id2 = payload["auth_user_id"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "hillary@gmail.com",
        "password": "123456789",
        "name_first": "Hillary",
        "name_last": "Clinton"
    })
    payload = r.json()
    token3 = payload["token"]

    # user1 creates a channel, adds user2 and sends a message
    # create channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel1",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # sends channel message
    msg = "Welcome"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()
    msg_id1 = payload["message_id"]

    # user1 creates dm with user2 and sends a message
    # creating dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token1,
        "u_ids": [u_id2]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]
    # dm message
    msg2 = "Hello George"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token1,
        "dm_id": dm_id1,
        "message": msg2
    })
    payload = r.json()
    msg_id2 = payload["message_id"]

    # user 2 reacts
    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 1
    })

    r = requests.post(f"{url}/message/react/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 1
    })

    # input error with invalid messageid
    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": 1234,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    # input error with invalid react id
    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 5
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 5
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    # user 2 unreacts
    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 1
    })

    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 1
    })

    # input error when user 2 tries to unreact again to same msg
    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": msg_id1,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token2,
        "message_id": msg_id2,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    # user3 trying to unreact
    # user3 trying to react
    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token3,
        "message_id": msg_id1,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.post(f"{url}/message/unreact/v1", json={
        "token": token3,
        "message_id": msg_id2,
        "react_id": 1
    })
    payload = r.json()
    assert payload["name"] == "System Error"
