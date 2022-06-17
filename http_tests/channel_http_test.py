import pytest
import requests
from src.other import clear_v1, load_data


url = "http://127.0.0.1:8080/"

def test_channel_invite_add_remove():
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
    u_id2 = payload["auth_user_id"]

    # Create test channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "test_channel",
        "is_public": True
    })
    payload = r.json()
    channel_id = payload["channel_id"]

    # Invite user 2 to channel
    r = requests.post(f"{url}/channel/invite/v2", json={
        "token": token1,
        "channel_id": channel_id,
        "u_id": u_id2
    })

    # Add user 2 as owner of channel
    r = requests.post(f"{url}/channel/addowner/v1", json={
        "token": token1,
        "channel_id": channel_id,
        "u_id": u_id2
    })

    # Removes users as owner of channel
    r = requests.post(f"{url}/channel/removeowner/v1", json={
        "token": token1,
        "channel_id": channel_id,
        "u_id": u_id2
    })
    payload = r.json()
    
    assert payload == {}


def test_join_details_leave():
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

    # Create test channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "test_channel",
        "is_public": True
    })
    payload = r.json()
    channel_id = payload["channel_id"]

    # User 2 joins channel
    r = requests.post(f"{url}/channel/join/v2", json={
        "token": token1,
        "channel_id": channel_id
    })

    # Provide basic details about channel
    r = requests.get(f"{url}/channel/details/v2", json={
        "token": token1,
        "channel_id": channel_id
    })

    # Show messages in channel
    r = requests.get(f"{url}/channel/messages/v2", json={
        "token": token1,
        "channel_id": channel_id,
        "start": 0
    })

    # User 2 leaves channel
    r = requests.get(f"{url}/channel/leave/v1", json={
        "token": token1,
        "channel_id": channel_id
    })
    payload = r.json()
    assert payload == {}
