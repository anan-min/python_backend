import pytest
import src.dm as dm
from src.other import clear_v1
from src.error import InputError, AccessError
from src.auth import auth_register_v2, auth_login_v2


@pytest.fixture
def users():
    clear_v1()
    r1 = auth_register_v2("test1@gmail.com", "password", "aa", "aa")
    r2 = auth_register_v2("test2@gmail.com", "password", "bb", "bb")
    r3 = auth_register_v2("test3@gmail.com", "password", "cc", "cc")
    r4 = auth_register_v2("test4@gmail.com", "password", "dd", "dd")

    return {
        "user1": r1,
        "user2": r2,
        "user3": r3,
        "user4": r4
    }


@pytest.fixture
def invalid_dm_id(users):
    user1 = users["user1"]
    user2 = users["user2"]
    users["user3"]
    user4 = users["user4"]

    token = user1["token"]
    u_ids = [user2["auth_user_id"]]

    r = dm.dm_create_v1(token, u_ids)
    dm_id = r["dm_id"] + 1
    u_id = user4["auth_user_id"]

    return {
        "token": token,
        "u_ids": u_ids,
        "u_id": u_id,
        "dm_id": dm_id,

    }


@pytest.fixture()
def non_authorised_user(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]
    user4 = users["user4"]

    token1 = user1["token"]
    u_ids = [user2["auth_user_id"]]

    r = dm.dm_create_v1(token1, u_ids)
    dm_id = r["dm_id"]
    token3 = user3["token"]  # user3 is not in dm
    u_id = user4["auth_user_id"]

    return {
        "token": token3,
        "dm_id": dm_id,
        "u_id": u_id,
        "u_ids": u_ids,
    }


# when u_id does not refers to a valid user
def test_dm_create_input_error(users):
    user1 = users["user1"]
    token = user1["token"]

    with pytest.raises(AccessError):
        dm.dm_create_v1(token,['not','an','id'])


def test_dm_create_success(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]

    assert dm.dm_create_v1(user1["token"], [user2["auth_user_id"], user3["auth_user_id"]]) == {
        "dm_id": 1000,
        "name": "aaaa, bbbb, cccc"
    }


#DM ID is not a valid DM
def test_dm_details_input_error(users,invalid_dm_id):
    token = invalid_dm_id["token"]
    dm_id = invalid_dm_id["dm_id"]
    with pytest.raises(InputError):
        dm.dm_details_v1(token, dm_id)


#Authorised user is not a member of this DM with dm_id
def test_dm_details_access_error(users, non_authorised_user):
    token = non_authorised_user["token"]
    dm_id = non_authorised_user["dm_id"]

    with pytest.raises(AccessError):
        dm.dm_details_v1(token, dm_id)


def test_dm_details_success(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]
    dm_info = dm.dm_create_v1(user1["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    assert dm.dm_details_v1(user1["token"], dm_info["dm_id"]) == {
        "name": dm_info["name"],
        "members": {
            "members": [f'{user2["auth_user_id"]}', f'{user3["auth_user_id"]}', f'{user1["auth_user_id"]}'],
            "owner": f'{user1["auth_user_id"]}',
        }
    }


def test_dm_list_success(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]
    dm_id = dm.dm_create_v1(user1["token"], [user2["auth_user_id"]])
    dm_id2 = dm.dm_create_v1(user1["token"], [user3["auth_user_id"]])

    assert dm_id2, dm_id in dm.dm_list_v1(user1["token"]).keys()


#dm_id does not refer to a valid DM
def test_dm_remove_input_error(users, invalid_dm_id):
    token = invalid_dm_id["token"]
    dm_id = invalid_dm_id["token"]

    with pytest.raises(InputError):
        dm.dm_remove_v1(token, dm_id)


#the user is not the original DM creator
def test_dm_remove_access_error(users, non_authorised_user):
    token = non_authorised_user["token"]
    dm_id = non_authorised_user["dm_id"]

    with pytest.raises(AccessError):
        dm.dm_remove_v1(token, dm_id)


def test_dm_remove_success(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]
    dm_info = dm.dm_create_v1(user1["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    assert dm.dm_remove_v1(user1["token"], dm_info["dm_id"]) == {}


#dm_id does not refer to an existing dm. u_id does not refer to a valid user. 
def test_dm_invite_input_error_1(users, invalid_dm_id):
    token = invalid_dm_id["token"]
    dm_id = invalid_dm_id["token"]
    u_id = invalid_dm_id["u_id"]

    with pytest.raises(InputError):
        dm.dm_invite_v1(token, dm_id, u_id)


#u_id does not refer to a valid user.
def test_dm_invite_input_error_2(users):
    user1 = users["user1"]
    user2 = users["user2"]

    token = user1["token"]
    u_ids = [user2["auth_user_id"]]

    r = dm.dm_create_v1(token, u_ids)
    dm_id = r["dm_id"]

    with pytest.raises(InputError):
        dm.dm_invite_v1(token, dm_id, "invalid u_id")

#the authorised user is not already a member of the DM
def test_dm_invite_access_error(users, non_authorised_user):
    token = non_authorised_user["token"]
    dm_id = non_authorised_user["dm_id"]
    u_id = non_authorised_user["u_id"]

    with pytest.raises(AccessError):
        dm.dm_invite_v1(token, dm_id, u_id)


def test_dm_invite_success(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]
    dm_info = dm.dm_create_v1(user1["token"], [user2["auth_user_id"]])

    assert dm.dm_invite_v1(user1["token"], dm_info["dm_id"], user3["auth_user_id"]) == {}


#dm_id is not a valid DM
def test_dm_leave_input_error(users, invalid_dm_id):
    token = invalid_dm_id["token"]
    dm_id = invalid_dm_id["dm_id"]

    with pytest.raises(InputError):
        dm.dm_leave_v1(token, dm_id)


#Authorised user is not a member of DM with dm_id
def test_dm_leave_access_error(users,non_authorised_user):
    token = non_authorised_user["token"]
    dm_id = non_authorised_user["dm_id"]

    with pytest.raises(AccessError):
        dm.dm_leave_v1(token, dm_id)


def test_dm_leave_success(users):
    user1 = users["user1"]
    user2 = users["user2"]
    user3 = users["user3"]
    dm_info = dm.dm_create_v1(user1["token"], [user2["auth_user_id"], user3["auth_user_id"]])

    assert dm.dm_leave_v1(user3["token"], dm_info["dm_id"]) == {}


#DM ID is not a valid DM
def test_dm_messages_input_error_1(users,invalid_dm_id):
    token = invalid_dm_id["token"]
    dm_id = invalid_dm_id["dm_id"]

    with pytest.raises(InputError):
        dm.dm_messages_v1(token, dm_id, 0)


#Authorised user is not a member of DM with dm_id
def test_dm_messages_access_error_2(users, non_authorised_user):
    token = non_authorised_user["token"]
    dm_id = non_authorised_user["dm_id"]

    with pytest.raises(AccessError):
        dm.dm_messages_v1(token, dm_id, 0)



