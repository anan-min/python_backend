from os import name
import requests
import json
import urllib
import pytest
from src.other import clear_v1
from src.error import InputError, AccessError

url = 'http://127.0.0.1:8080/'
def test_standup_start_active_send():
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
    
    # Create test channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "test_channel",
        "is_public": True
    })
    payload = r.json()
    channel_id = payload["channel_id"]

    #start test_standup
    r = requests.post(f"{url}/standup/start/v1", json={
        "token": token1,
        "channel_id": channel_id,
        "length": 50
    })
    payload = r.json()
    time_finish = payload["time_finish"]

    #check active of standup
    r = requests.get(f"{url}/standup/active/v1", json={
        "token": token1,
        "channel_id": channel_id
    })
    payload = r.json()
    check_time_finish = payload["time_finish"]
    is_active = payload["is_active"]

    assert time_finish == check_time_finish
    assert is_active == True

    #check send standup
    r = requests.post(f"{url}/standup/send/v1", json={
        "token": token1,
        "channel_id": channel_id,
        "message": "hello"
    })
    payload = r.json()
    
    assert payload == {}
    
