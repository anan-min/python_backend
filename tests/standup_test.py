"""
Author: Zhitong Chen 
Date: 2021/4/16
Content: All funtion tests for standup functions
"""
import pytest
from src.other import clear_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError

@pytest.fixture
def users():
    clear_v1()
    r1 = auth_register_v2("test1@gmail.com", "password", "aa", "aa")
    r2 = auth_register_v2("test2@gmail.com", "password", "bb", "bb")
    
    return {
        "user1": r1,
        "user2": r2
    }

@pytest.fixture
def invalid_channel_id(users):
    user1 = users["user1"]
    token = user1["token"]

    channel = channels_create_v2(token, "testchannel", True)
    channel_id = channel["channel_id"] + 1

    return {
        "channel_id": channel_id
    }

@pytest.fixture
def valid_channel_id(users):
    user1 = users["user1"]
    token = user1["token"]

    channel = channels_create_v2(token, "testchannel", True)
    channel_id = channel["channel_id"]

    return {
        "channel_id": channel_id
    }
   

def test_start_invalid_channel_id(users, invalid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = invalid_channel_id["channel_id"]

    with pytest.raises(InputError):
        standup_start_v1(token, channel_id, 50)

def test_start_user_not_in_channel(users, valid_channel_id):
    user = users["user2"]
    invalid_token = user["token"]
    channel_id = valid_channel_id["channel_id"]

    with pytest.raises(AccessError):
        standup_start_v1(invalid_token, channel_id, 50)

def test_start_standup_exists(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    standup_start_v1(token, channel_id, 50)


    with pytest.raises(InputError):
        standup_start_v1(token, channel_id, 50)

def test_standup_start_success(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    info1 = standup_start_v1(token, channel_id, 50)
    info2 = standup_active_v1(token, channel_id)

    assert info1["time_finish"] == info2["time_finish"]

def test_active_invalid_channel_id(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    invalid_channel_id = channel_id + 1
    standup_start_v1(token, channel_id, 50)

    with pytest.raises(InputError):
        standup_active_v1(token, invalid_channel_id)

def test_standup_active_success(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    info = standup_start_v1(token, channel_id, 50)

    assert standup_active_v1(token, channel_id) == {
        "is_active": True,
        "time_finish": info["time_finish"]
    }

def test_send_invalid_channel_id(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    invalid_channel_id = channel_id + 1
    standup_start_v1(token, channel_id, 50)

    with pytest.raises(InputError):
        standup_send_v1(token, invalid_channel_id, "hello")

def test_send_standup_not_exist(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]

    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, "hello")

def test_send_user_not_in_channel(users, valid_channel_id):
    user = users["user2"]
    invalid_token = user["token"]
    valid_user = users["user1"]
    token = valid_user["token"]
    channel_id = valid_channel_id["channel_id"]
    standup_start_v1(token, channel_id, 50)

    with pytest.raises(AccessError):
        standup_send_v1(invalid_token, channel_id, "hello")

def test_send_over_thousand_message(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    standup_start_v1(token, channel_id, 50)

    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, "oops" * 1000)

def test_standup_send_success(users, valid_channel_id):
    user = users["user1"]
    token = user["token"]
    channel_id = valid_channel_id["channel_id"]
    standup_start_v1(token, channel_id, 50)

    assert standup_send_v1(token, channel_id, "hello") == {}
