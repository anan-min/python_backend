from os import name
import requests
import json
import urllib
import pytest
from src.other import clear_v1
from src.error import InputError, AccessError

base_url = 'http://127.0.0.1:8080/'
def test_dm_create():
    clear_v1()
    create_url = base_url + "/dm/create/v1"
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    u_id = payload2["auth_user_id"]

    #when u_id not refers to a valid user
    invalid_u_id = requests.post(create_url, json = {
        "token": token,
        "u_ids": "88" #not a valid user
    })
    payload = invalid_u_id.json()
    assert payload["name"] == "System Error"

    #success
    response = requests.post(create_url, json = {
        "token": token,
        "u_ids": u_id
    })
    payload3 = response.json()
    assert payload3['name'] != 'System Error'

def test_dm_details():
    clear_v1()
    details_url = base_url + "/dm/details/v1"

    #create sample user
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    u_id = payload2["auth_user_id"]
    user3 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail3@email.com",
        "password": "password",
        "name_first": "cc",
        "name_last": "cc" 
    })
    payload3 = user3.json()
    invalid_token = payload3["token"]

    #create dm channel
    dm = requests.post(f"{base_url}/dm/create/v1", json = {
        "token": token,
        "u_ids": u_id
    })
    payload4 = dm.json()
    dm_id = payload4["dm_id"]

    #when dm_id is not valid
    detail1 = requests.get(details_url, json = {
        "token": token,
        "dm_id": "9999" #invalid dm_id
    })
    detail1 = detail1.json()
    assert detail1['name'] == 'System Error'

    #when token is not valid
    detail2 = requests.get(details_url, json = {
        "token": invalid_token,
        "dm_id": dm_id
    })
    detail2 = detail2.json()
    assert detail2['name'] == 'System Error'

    #success
    detail3 = requests.get(details_url, json = {
        "token": token,
        "dm_id": dm_id
    })
    assert detail3.status_code == 200

def test_dm_list():
    clear_v1()
    list_url = base_url + "/dm/list/v1"

    #create sample user
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    u_id = payload2["auth_user_id"]

    #create sample dm
    requests.post(f"{base_url}/dm/create/v1", json = {
        "token": token,
        "u_ids": u_id
    })

    #success
    dm_list = requests.get(list_url, json = {
        "token": token
    })
    
    assert dm_list.status_code == 200

def test_dm_remove():
    clear_v1()
    remove_url = base_url + "/dm/remove/v1"

    #create sample user
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    u_id = payload2["auth_user_id"]
    invalid_token = payload2["token"]

    #create sample dm
    dm = requests.post(f"{base_url}/dm/create/v1", json = {
        "token": token,
        "u_ids": u_id
    })
    payload3 = dm.json()
    dm_id = payload3["dm_id"]

    #when dm_id is not valid
    result1 = requests.delete(remove_url, json = {
        "token": token,
        "dm_id": 9999 #invalid dm_id
    })
    result1 = result1.json()
    assert result1['name'] == 'System Error'

    #when token is not refers to the creator of the channel(invalid)
    result2 = requests.delete(remove_url,json = {
        "token": invalid_token,
        "dm_id": dm_id
    })
    result2 = result2.json()
    assert result2['name'] == 'System Error'

    #success
    result3 = requests.delete(remove_url, json = {
        "token": token,
        "dm_id": dm_id
    })
    assert result3.status_code == 200

def test_dm_invite():
    clear_v1()
    invite_url = base_url + "/dm/invite/v1"

    #create sample user
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    u_id = payload2["auth_user_id"]
    user3 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail3@email.com",
        "password": "password",
        "name_first": "cc",
        "name_last": "cc" 
    })
    payload3 = user3.json()
    invite_u_id = payload3["auth_user_id"]

    #create dm channel
    dm = requests.post(f"{base_url}/dm/create/v1", json = {
        "token": token,
        "u_ids": u_id
    })
    payload4 = dm.json()
    dm_id = payload4["dm_id"]

    #when dm_id is invalid
    result1 = requests.post(invite_url, json = {
        "token": token,
        "dm_id": "9999",
        "u_id": invite_u_id
    })
    payload5 = result1.json()
    assert payload5['name'] == 'System Error'

    #u_id does not refers to a valid user
    result2 = requests.post(invite_url, json = {
        "token": token,
        "dm_id": dm_id,
        "u_id": "invalid_u_id"
    })
    payload6 = result2.json()
    assert payload6['name'] == 'System Error'

    #when authorised user is not a member of dm
    result = requests.post(invite_url, json = {
        "token": "invalid_token",
        "dm_id": dm_id,
        "u_id": invite_u_id
    })

    #success
    result = requests.post(invite_url, json = {
        "token": token,
        "dm_id": dm_id,
        "u_ids": invite_u_id
    })
    assert result.status_code == 200

def test_dm_leave():
    clear_v1()
    leave_url = base_url + "/dm/leave/v1"

    #create sample user
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    u_id = payload2["auth_user_id"]
    leave_token = payload2["token"]
    user3 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail3@email.com",
        "password": "password",
        "name_first": "cc",
        "name_last": "cc" 
    })
    payload3 = user3.json()
    invalid_token = payload3["token"]

    #create dm channel
    dm = requests.post(f"{base_url}/dm/create/v1", json = {
        "token": token,
        "u_ids": u_id
    })
    payload4 = dm.json()
    dm_id = payload4["dm_id"]

    #when dm_id is not valid
    result1 = requests.post(leave_url, json = {
        "token": leave_token,
        "dm_id": "9999" #invalid_dm_id
    })
    payload5 = result1.json()
    assert payload5['name'] == 'System Error'

    #when token is not refer to a member of dm
    result2 = requests.post(leave_url, json = {
        "token": invalid_token,
        "dm_id": dm_id
    })
    payload6 = result2.json()
    assert payload6['name'] == 'System Error'

    #success
    result3 = requests.post(leave_url, json = {
        "token": leave_token,
        "dm_id": dm_id
    })
    assert result3.status_code == 200

def test_dm_messages():
    clear_v1()
    messages_url = base_url + "/dm/messages/v1"

    #create sample user1
    user1 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail1@email.com",
        "password": "password",
        "name_first": "aa",
        "name_last": "aa" 
    })
    payload1 = user1.json()
    token = payload1["token"]

    #create sample user2
    user2 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail2@email.com",
        "password": "password",
        "name_first": "bb",
        "name_last": "bb" 
    })
    payload2 = user2.json()
    token2 = payload2["token"]
    u_id = payload2["auth_user_id"]

    user3 = requests.post(f"{base_url}/auth/register/v2", json = {
        "email": "testemail3@email.com",
        "password": "password",
        "name_first": "cc",
        "name_last": "cc" 
    })
    payload3 = user3.json()
    invalid_token = payload3["token"]

    #create dm channel
    dm = requests.post(f"{base_url}/dm/create/v1", json = {
        "token": token,
        "u_ids": u_id
    })
    payload4 = dm.json()
    dm_id = payload4["dm_id"]

    #send message in dm
    requests.post(f"{base_url}/messsage/senddm/v1", json = {
        "token": token2,
        "dm_id": dm_id,
        "message": "Hello"
    })

    #when dm_id is not valid
    result1 = requests.get(messages_url, json = {
        "token": token,
        "dm_id": "9999",
        "start": "0"
    })
    payload5 = result1.json()
    assert payload5['name'] == 'System Error'

    #when authorised user is not a member of dm
    result2 = requests.get(messages_url, json = {
        "token": invalid_token,
        "dm_id": dm_id,
        "start": "0"
    })
    payload6 = result2.json()
    assert payload6['name'] == 'System Error'

    #success
    result3 = requests.get(f"{base_url}/dm/messages/v1", json = {
        "token": token,
        "dm_id": dm_id,
        "start": "0"
    })
    payload = result3.json()
    assert payload['name'] == 'System Error'

# test for new function in this iteration









    
