import requests
from src.other import clear_v1
from src.error import InputError, AccessError

url = "http://127.0.0.1:8080/"


def test_clear_v1_simple():
    clear_v1()

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

    # create 5 channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Another Channel",
        "is_public": True
    })
    payload = r.json()

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Public Channel",
        "is_public": False
    })
    payload = r.json()

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Some Channel",
        "is_public": False
    })
    payload = r.json()

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Last Channel",
        "is_public": True
    })
    payload = r.json()

    # clear
    clear_v1()

    # register user2
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]

    # create a channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Georges Channel",
        "is_public": True
    })
    payload = r.json()
    channelid2 = payload["channel_id"]

    # listall
    r = requests.get(f"{url}/channels/listall/v2", json={
        "token": token2
    })
    payload = r.json()

    expectedoutput = {
						'channels':
							[
								{'channel_id':channelid2,'name':'Georges Channel'}
							]
					}
    assert payload == expectedoutput


def test_clear_v1_errors():
    clear_v1()

    # New user created
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

    # clear
    clear_v1()

    # trying to log in with cleared user credentials
    r = requests.post(f"{url}/auth/login/v1", json={
        "email": 'camila@gmail.com',
        "password": '123456789'
    })
    payload = r.json()
    
    assert payload["name"] == "System Error"

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]
    u_id1 = payload["auth_user_id"]

    # clear
    clear_v1()

    # register user 2
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Georges Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id2 = payload["channel_id"]

    # try to invite cleared user
    r = requests.post(f"{url}/channel/invite/v1", json={
        "token": token2,
        "channel_id": channel_id2,
        "u_id": u_id1
    })
    payload = r.json()

    assert payload["name"] == "System Error"

    # clear
    clear_v1()

    # Creating a user and channel
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

    # create a channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # Clear
    clear_v1()

    # Creating user again
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # trying to pull details about cleared channel
    r = requests.get(f"{url}/channel/details/v1", json={
        "token": token1,
        "channel_id": channel_id1
    })
    payload = r.json()
    
    assert payload["name"] == "System Error"

def test_search_nomessages():
    # clear
    clear_v1()

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

    # search
    r = requests.get(f"{url}/search/v2", json={
        "token": token,
        "query_str": "Message"
    })
    payload = r.json()
    expectedoutput = {"messages":[]}

    assert payload == expectedoutput


def test_onemessage():
    # clear
    clear_v1()

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

    # channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # message
    msg = "This is a message"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()
    m_id = payload["message_id"]
    

    # search
    strg = "message"

    r = requests.get(f"{url}/search/v2", json={
        "token": token,
        "query_str": strg
    })
    payload = r.json()

    expectedoutput = (m_id)
    assert (payload["messages"][0]["message_id"]) == expectedoutput


def test_multipledm():
    # clear
    clear_v1()

    # register 3 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

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
        "email": "adam@gmail.com",
        "password": "123456789",
        "name_first": "Adam",
        "name_last": "Eve"
    })
    payload = r.json()
    u_id3 = payload["auth_user_id"]

    # new dms
    # user 1 creates dm with user 2
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token,
        "u_ids": [u_id2]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]
    # user 2 creates dm with user 3
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token2,
        "u_ids": [u_id3]
    })
    payload = r.json()
    dm_id2 = payload["dm_id"]

    # sending messages
    msg = "This is a message"
    msg2 = 'This is also a message'
    # user 1 sends message to user 2
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token2,
        "dm_id": dm_id1,
        "message": msg
    })
    payload = r.json()
    m_id1 = payload["message_id"]
    
    # user 2 sends message to user 3
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token2,
        "dm_id": dm_id2,
        "message": msg2
    })
    payload = r.json()
    m_id2 = payload["message_id"]

    # search
    strng = 'message'

    r = requests.get(f"{url}/search/v2", json={
        "token": token2,
        "query_str": strng
    })
    payload = r.json()

    expectedoutput = (m_id1,m_id2)

    assert (payload["messages"][0]["message_id"], payload["messages"][1]["message_id"]) == expectedoutput


def test_multiplemessages():
    # clear
    clear_v1()

    # register 2 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]

    # create 2 channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Georges Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id6 = payload["channel_id"]

    # messages
    msg = "This is a message"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token2,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()
    m_id1 = payload["message_id"]

    msg2 = "Another message"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token2,
        "channel_id": channel_id6,
        "message": msg2
    })
    payload = r.json()
    m_id2 = payload["message_id"]

    # search
    strng = "message"

    r = requests.get(f"{url}/search/v2", json={
        "token": token2,
        "query_str": strng
    })
    payload = r.json()

    expectedoutput = (m_id1,m_id2)

    assert (payload["messages"][0]["message_id"], payload["messages"][1]["message_id"]) == expectedoutput

def test_dmandmessages():
    # clear
    clear_v1()

    # register 2 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]
    u_id1 = payload["auth_user_id"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]

    # create a channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # create dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token2,
        "u_ids": [u_id1]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]

    # messages
    msg = "This is a message"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token2,
        "dm_id": dm_id1,
        "message": msg
    })
    payload = r.json()
    m_id = payload["message_id"]

    msg2 = "Another message"
    r = requests.post(f"{url}/message/send/v2", json={
        "token": token,
        "channel_id": channel_id1,
        "message": msg2
    })
    payload = r.json()
    m_id2 = payload["message_id"]

    expectedoutput = (m_id,m_id2)

    r = requests.get(f"{url}/search/v2", json={
        "token": token,
        "query_str": "message"
    })
    payload = r.json()
    
    assert (payload["messages"][0]["message_id"], payload["messages"][1]["message_id"]) == expectedoutput


def test_search_error():
    # clear
    clear_v1()

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token = payload["token"]

    # search 1
    strng = 'i' * 20000
    r = requests.get(f"{url}/search/v2", json={
        "token": token,
        "query_str": strng
    })
    payload = r.json()

    assert payload["name"] == "System Error"

    # search 2
    strng2 = 'i' * 1001
    r = requests.get(f"{url}/search/v2", json={
        "token": token,
        "query_str": strng2
    })
    payload = r.json()

    assert payload["name"] == "System Error"
    
