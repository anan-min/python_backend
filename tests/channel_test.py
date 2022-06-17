"""Test functions for channel.py"""
import pytest

from src.channel import channel_details_v2, channel_invite_v2, channel_join_v2, channel_messages_v2, channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import AccessError, InputError
from src.other import clear_v1
from src.utils import load_data

def test_channel_invite_v2():
    """Testing channel_invite_v2() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Public channel_id: 1, 2
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)
    channel2 = channels_create_v2(user1["token"], "test_channel_2", True)

    # invalid channel_id
    with pytest.raises(InputError):
        channel_invite_v2(user1["token"], 6, user2["auth_user_id"])

    # invalid u_id
    with pytest.raises(InputError):
        channel_invite_v2(user1["token"], channel2["channel_id"], 6)

    # authorised user is not member of channel
    with pytest.raises(AccessError):
        channel_invite_v2(user3["token"], channel1["channel_id"], user2["auth_user_id"])

    # successful invite
    assert channel_invite_v2(user1["token"], channel1["channel_id"], user2["auth_user_id"]) == {}


def test_channel_details_v2():
    """Testing channel_details_v2() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)

    # invalid channel_id
    with pytest.raises(InputError):
        channel_details_v2(user1["token"], 6)

    # authorised user is not member of channel
    with pytest.raises(AccessError):
        channel_details_v2(user2["token"], channel1["channel_id"])

    # successful channel details
    assert channel_details_v2(user1["token"], channel1["channel_id"]) == {
        "name": "test_channel_1",
        "owner_members": [
            {
                "u_id": 1000,
                "email": "mail1@mail.com",
                "name_first": "First",
                "name_last": "Last",
                "handle_str": "firstlast"
            }
        ],
        "all_members": [
            {
                "u_id": 1000,
                "email": "mail1@mail.com",
                "name_first": "First",
                "name_last": "Last",
                "handle_str": "firstlast"
            }
        ],
    }


def test_channel_messages_v2():
    """Testing channel_messages_v2() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)

    data = load_data()

    data["messages"][str(channel1["channel_id"])] = {
        "messages": [
            {
                "message_id": 1,
                "u_id": 0,
                "message": "Hello world",
                "time_created": 1582426789,
                'is_pinned': False,
            }
        ],
    }
    # invalid channel_id
    with pytest.raises(InputError):
        channel_messages_v2(user1["token"], 20, 0)

    # start > total num of messages
    with pytest.raises(InputError):
        channel_messages_v2(user1["token"], channel1["channel_id"], 600)

    # authorised user is not member of channel
    with pytest.raises(AccessError):
        channel_messages_v2(user2["token"], channel1["channel_id"], 0)

    """
    # successful retrieval
    success_msg = {"messages": data["messages"][channel1_id]["messages"], "start": 0, "end": -1}
    assert channel_messages_v2(user1["token"], channel1_id, 0) == success_msg
    # there is no data["messages"]["u_id"] created
    """


def test_channel_leave_v1():
    """Testing channel_leave_v1() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")
    user4 = auth_register_v2("mail4@mail.com", "password", "Fourth", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)
    
    # Add users to channel with channel_id 1
    channel_join_v2(user2["token"], channel1["channel_id"])
    channel_join_v2(user3["token"], channel1["channel_id"])

    # Success: users leaving channel
    assert channel_leave_v1(user2["token"], channel1["channel_id"]) == {}
    
    assert channel_leave_v1(user3["token"], channel1["channel_id"]) == {}

    # InputError: invalid channel_id
    with pytest.raises(InputError):
        channel_leave_v1(user4["token"], 2)
    
    with pytest.raises(InputError):
        channel_leave_v1(user2["token"], 3)
    
    # AccessError: authorised user is not a member of channel with channel_id
    with pytest.raises(AccessError):
        channel_leave_v1(user2["token"], channel1["channel_id"])
    
    with pytest.raises(AccessError):
        channel_leave_v1(user4["token"], channel1["channel_id"])


def test_channel_join_v2():
    """Testing channel_join_v2() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Public channel_id: 1
    # Private channel_id: 2
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)
    channel2 = channels_create_v2(user1["token"], "test_channel_2", False)

    # Success: add users to valid channel
    assert channel_join_v2(user2["token"], channel1["channel_id"]) == {}

    assert channel_join_v2(user3["token"], channel1["channel_id"]) == {} 

    # InputError: invalid channel_id
    with pytest.raises(InputError):
        channel_join_v2(user2["token"], 3)
    
    with pytest.raises(InputError):
        channel_join_v2(user3["token"], 4)
    
    # AccessError: private channel
    with pytest.raises(AccessError):
        channel_join_v2(user2["token"], channel2["channel_id"])

    with pytest.raises(AccessError):
        channel_join_v2(user3["token"], channel2["channel_id"])


def test_channel_addowner_v1():
    """Testing channel_addowner_v1() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")
    user4 = auth_register_v2("mail4@mail.com", "password", "Fourth", "Last")
    user5 = auth_register_v2("mail5@mail.com", "password", "Fifth", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)

    # Success: add owner to valid channel
    assert channel_addowner_v1(user1["token"], channel1["channel_id"], user2["auth_user_id"]) == {}

    assert channel_addowner_v1(user2["token"], channel1["channel_id"], user3["auth_user_id"]) == {}

    # InputError: invalid channel_id
    with pytest.raises(InputError):
        channel_addowner_v1(user3["token"], 5, user1["auth_user_id"])

    with pytest.raises(InputError):
        channel_addowner_v1(user1["token"], 4, user2["auth_user_id"])

    # InputError: user with u_id is already owner of channel
    with pytest.raises(InputError):
        channel_addowner_v1(user2["token"], channel1["channel_id"], user1["auth_user_id"])
    
    with pytest.raises(InputError):
        channel_addowner_v1(user3["token"], channel1["channel_id"], user2["auth_user_id"])
    
    # AccessError: authorised user is not owner of channel
    # Add user4 as member of channel1
    channel_join_v2(user4["token"], channel1["channel_id"])
    with pytest.raises(AccessError):
        channel_addowner_v1(user4["token"], channel1["channel_id"], user3["auth_user_id"]) # Expect fail as user4 is member NOT owner of channel1
    
    with pytest.raises(AccessError):
        channel_addowner_v1(user5["token"], channel1["channel_id"], user1["auth_user_id"]) # Expect fail as user5 is not member or owner of channel1


def test_channel_removeowner_v1():
    """Testing channel_removeowner_v1() function"""
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")
    user4 = auth_register_v2("mail4@mail.com", "password", "Fourth", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1["token"], "test_channel_1", True)

    # Add owners to channel
    channel_addowner_v1(user1["token"], channel1["channel_id"], user2["auth_user_id"])
    channel_addowner_v1(user2["token"], channel1["channel_id"], user3["auth_user_id"])
    channel_addowner_v1(user3["token"], channel1["channel_id"], user4["auth_user_id"])

    # Success: remove owner from valid channel
    assert channel_removeowner_v1(user2["token"], channel1["channel_id"], user3["auth_user_id"]) == {}

    assert channel_removeowner_v1(user1["token"], channel1["channel_id"], user2["auth_user_id"]) == {}

    # InputError: invalid channel_id
    with pytest.raises(InputError):
        channel_removeowner_v1(user3["token"], 2, user2["auth_user_id"])
    
    with pytest.raises(InputError):
        channel_removeowner_v1(user2["token"], 3, user1["auth_user_id"])
    
    # InputError: user with u_id is not owner of channel
    with pytest.raises(InputError):
        channel_removeowner_v1(user1["token"], channel1["channel_id"], user2["auth_user_id"])
    
    with pytest.raises(InputError):
        channel_removeowner_v1(user1["token"], channel1["channel_id"], user3["auth_user_id"])

    # InputError: user is currently the only owner
    # Remove user4 as owner
    assert channel_removeowner_v1(user1["token"], channel1["channel_id"], user4["auth_user_id"]) == {}

    with pytest.raises(InputError):
        channel_removeowner_v1(user1["token"], channel1["channel_id"], user3["auth_user_id"])

    with pytest.raises(InputError):
        channel_removeowner_v1(user1["token"], channel1["channel_id"], user2["auth_user_id"])
    
    # AccessError: authorised user is not owner of channel
    # Add user2 as member of channel1
    channel_join_v2(user2["token"], channel1["channel_id"])
    with pytest.raises(AccessError):
        channel_removeowner_v1(user2["token"], channel1["channel_id"], user1["auth_user_id"]) # Expect fail since user2 is member not owner of channel1
    
    with pytest.raises(AccessError):
        channel_removeowner_v1(user3["token"], channel1["channel_id"], user1["auth_user_id"]) # Expect fail since user3 is not member of owner of channel1
