import requests 
from src.other import clear_v1
from src.error import InputError, AccessError

url = "http://127.0.0.1:8080/"

def test_admin_user_permission():
    clear_v1()
    #Creating three users 
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
        "email": "third@gmail.com",
        "password": "123456789",
        "name_first": "Third",
        "name_last": "User"
    })
    payload = r.json()
    u_id3 = payload["auth_user_id"]

    #User2 (not owner) tying to make user3 an owner
    r = requests.post(f"{url}/admin/userpermission/change/v1", json={
        "token": token2,
        "uid": u_id3,
        "permission_id": 1})
    payload = r.json()

    assert payload["name"] == "System Error"
    
    #Trying to add owner using invalid u_id
    r = requests.post(f"{url}/admin/userpermission/change/v1", json={
        "token": token2,
        "uid": 'hello',
        "permission_id": 1})
    payload = r.json()

    assert payload["name"] == "System Error"
    
    r = requests.post(f"{url}/admin/userpermission/change/v1", json={
        "token": token2,
        "uid": 999999999999,
        "permission_id": 1})
    payload = r.json()

    assert payload["name"] == "System Error"

    #Using invalid permission_id
    r = requests.post(f"{url}/admin/userpermission/change/v1", json={
        "token": token1,
        "uid": u_id3,
        "permission_id": 5})
    payload = r.json()

    assert payload["name"] == "System Error"

    #User1 making user2 an owener
    r = requests.post(f"{url}/admin/userpermission/change/v1", json={
        "token": token1,
        "uid": u_id2,
        "permission_id": 1})
    payload = r.json()

    #User2 making user1 a member only then removing them from Dreams
    r = requests.post(f"{url}/admin/userpermission/change/v1", json={
        "token": token2,
        "uid": u_id1,
        "permission_id": 2})
    payload = r.json()

    r = requests.delete(f"{url}/admin/user/remove/v1", json={
        "token": token2,
        "uid": u_id1})
    payload = r.json()
    
    r = requests.get(f"{url}/user/profile/v2", json={
        "token": token2,
        "u_id": u_id1})
    payload = r.json()
    fname = payload["name_first"]

    assert fname == 'Removed'

def test_admin_remove():
    clear_v1()

    #creating two users 
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
    
    #User2 sends message to user1
    # create dm
    r = requests.post(f"{url}/dm/create/v1", json={
        "token": token2,
        "u_ids": [u_id1]
    })
    payload = r.json()
    dm_id1 = payload["dm_id"]

    # messages
    msg = "@camilamoro"
    r = requests.post(f"{url}/message/senddm/v1", json={
        "token": token2,
        "dm_id": dm_id1,
        "message": msg
    })
    payload = r.json()

    #Trying to remove a user with invalid user id
    r = requests.delete(f"{url}/admin/user/remove/v1", json={
        "token": token2,
        "uid": "hello"})
    payload = r.json()
    assert payload["name"] == "System Error"

    r = requests.delete(f"{url}/admin/user/remove/v1", json={
        "token": token2,
        "uid": 9999999999})
    payload = r.json()
    assert payload["name"] == "System Error"

    #User1 removes user2
    r = requests.delete(f"{url}/admin/user/remove/v1", json={
        "token": token1,
        "uid": u_id2})
    payload = r.json()

    #Checking if removal has been successful
    r = requests.get(f"{url}/user/profile/v2", json={
        "token": token1,
        "u_id": u_id2})
    payload = r.json()
    fname = payload["name_first"]

    assert fname == 'Removed'   

    #Creating user2 again
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]
    u_id2 = payload["auth_user_id"]

    #User2 trying to remove user1 (owner of dreams)
    r = requests.delete(f"{url}/admin/user/remove/v1", json={
        "token": token2,
        "uid": u_id1})
    payload = r.json()

    assert payload["name"] == "System Error"

    #User1 trying to remove themselves
    r = requests.delete(f"{url}/admin/user/remove/v1", json={
        "token": token1,
        "uid": u_id1})
    payload = r.json()

    assert payload["name"] == "System Error"
