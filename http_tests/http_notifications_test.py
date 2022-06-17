import requests 
from src.other import clear_v1

url = "http://127.0.0.1:8080/"

def test_get():
    clear_v1()
    # register 2 users
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

    # create a channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]
    
    # user 1 invites user 2 to channel
    r = requests.post(f"{url}/channel/invite/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "u_id": u_id2
    })
    payload = r.json()

    #message
    msg = "Welcome @georgebush"
    r = requests.post(f"{url}/message/send/v2=", json={
        "token": token1,
        "channel_id": channel_id1,
        "message": msg
    })
    payload = r.json()

    #User one created a new DM with user 2 and sends a message
    # new dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token1,
        "u_ids": [u_id2]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]

    # dm message
    msg2 = "Hello @georgebush"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token1,
        "dm_id": dm_id1,
        "message": msg2
    })
    payload = r.json()

    #Expected output
    notificationsoutput = {"notifications":
    [
        {
            'channel_id': -1, 
            'dm_id': dm_id1,
            'notification_message' : "camilamoro tagged you in camilamoro, georgebush: Hello @georgebush"
        },
        {
            'channel_id': -1, 
            'dm_id': dm_id1,
            'notification_message' : "camilamoro added you to camilamoro, georgebush"
        },
        {
            'channel_id': channel_id1, 
            'dm_id': -1,
            'notification_message' : "camilamoro tagged you to Private Channel: Welcome @georgebush"
        },
        {
            'channel_id': channel_id1, 
            'dm_id': -1,
            'notification_message' : "camilamoro added you to Private Channel"
        },
    ]}

    r = requests.get(f"{url}/notifications/get/v1", json={
        "token": token2
    })
    payload = r.json()    

    assert payload == notificationsoutput
