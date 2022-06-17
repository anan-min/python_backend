"""Importing functions"""
import pytest
import datetime
import time
import threading

from src.message import message_send_v2, message_remove_v1, message_edit_v2, message_share_v1, message_react_v1, message_unreact_v1, message_senddm_v1, message_pin_v1, message_unpin_v1, message_sendlater_v1, message_sendlaterdm_v1
from src.channel import channel_join_v2, channel_messages_v2, channel_invite_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import AccessError, InputError
from src.other import clear_v1, search_v1
from src.utils import load_data, token_to_id
from src.notifications import notifications_get_v1

def test_message_send_v2():
    '''Testing message_send_v2() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1['token'], "test_channel_1", True)

    # Add user2 to channel1 as member
    channel_join_v2(user2['token'], channel1["channel_id"])

    # Success: send message from authorised user to channel
    message_send_v2(user1['token'], channel1["channel_id"], "hello!")
    m_list = channel_messages_v2(user1['token'], channel1, 0)
    message_send_v2(user2['token'], channel1["channel_id"], "hey user1")


    # Messages should appear in channel_messages
    m_list = channel_messages_v2(user1['token'], channel1, 0)
    assert len(m_list['messages']) == 2

    message_send_v2(user1['token'], channel1["channel_id"], "how are you :)")
    message_send_v2(user2['token'], channel1["channel_id"], "not behd")

    m_list_2 = channel_messages_v2(user2['token'], channel1, 0)
    assert len(m_list_2['messages']) == 4

    # InputError: message is more than 1000 characters
    with pytest.raises(InputError):
        message_send_v2(user1['token'], channel1["channel_id"], "1001 dalmations" * 100)
    
    with pytest.raises(InputError):
        message_send_v2(user2['token'], channel1["channel_id"], "oops" * 1000)
    
    # AccessError: authorised user hasn't joined channel they're trying to post to
    with pytest.raises(AccessError):
        message_send_v2(user3['token'], channel1["channel_id"], "let me in")
    
    with pytest.raises(AccessError):
        message_send_v2(user3['token'], channel1["channel_id"], "guys im lonely")


def test_message_remove_v1():
    '''Testing message_remove_v1() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")
    user4 = auth_register_v2("mail4@mail.com", "password", "Fourth", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1['token'], "test_channel_1", True)

    # Add users 2-4 to channel1
    channel_join_v2(user2['token'], channel1["channel_id"])
    channel_join_v2(user3['token'], channel1["channel_id"])
    channel_join_v2(user4['token'], channel1["channel_id"])

    # Send messages to channel1
    message_0 = message_send_v2(user1['token'], channel1["channel_id"], "hello")
    message_1 = message_send_v2(user2['token'], channel1["channel_id"], "hey")
    message_2 = message_send_v2(user3['token'], channel1["channel_id"], "hi")

    # Success: message removed from channel
    m_list_before_removal = channel_messages_v2(user1['token'], channel1["channel_id"], 0)
    assert len(m_list_before_removal['messages']) == 3

    message_remove_v1(user1['token'], message_0["message_id"])
    m_list_after_first_removal = channel_messages_v2(user1['token'], channel1["channel_id"], 0)
    assert len(m_list_after_first_removal['messages']) == 2

    message_remove_v1(user2['token'], message_1["message_id"])
    m_list_after_second_removal = channel_messages_v2(user2['token'], channel1["channel_id"], 0)
    assert len(m_list_after_second_removal['messages']) == 1

    # Create DM between user1 and user2 and send messages
    dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm_id = dm['dm_id']

    dm_0 = message_senddm_v1(user1['token'], dm_id, "hi user2")
    dm_1 = message_senddm_v1(user2['token'], dm_id, "hey user1")

    # Success: message removed from DM
    dms_before_removal = dm_messages_v1(user1['token'], dm_id, 0)
    assert len(dms_before_removal['messages']) == 2


    message_remove_v1(user1['token'], dm_0)
    dms_after_first_removal = dm_messages_v1(user1['token'], dm_id, 0)
    assert len(dms_after_first_removal['messages']) == 1


    message_remove_v1(user2['token'], dm_1)
    dms_after_second_removal = dm_messages_v1(user2['token'], dm_id, 0)
    assert dms_after_second_removal == None    

    # InputError: message_id no longer exists
    with pytest.raises(InputError):
        message_remove_v1(user1['token'], message_0["message_id"])
    
    with pytest.raises(InputError):
        message_remove_v1(user2['token'], message_1["message_id"])
    
    # AccessError: message removed by user who didn't send it and isn't owner of channel
    with pytest.raises(AccessError):
        message_remove_v1(user2['token'], message_2["message_id"])
    
    with pytest.raises(AccessError):
        message_remove_v1(user4['token'], message_2["message_id"])

    
def test_message_edit_v2():
    '''Testing message_edit_v2() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Public channel_id: 1
    channel1 = channels_create_v2(user1['token'], "test_channel_1", True)

    # Add users to channel
    channel_join_v2(user2['token'], channel1["channel_id"])
    channel_join_v2(user3['token'], channel1["channel_id"])

    # Send messages to channel1
    message_0 = message_send_v2(user1['token'], channel1["channel_id"], "hello")
    message_1 = message_send_v2(user2['token'], channel1["channel_id"], "hey")
    message_2 = message_send_v2(user3['token'], channel1["channel_id"], "hi")

    # Success: message updated with new text
    data = load_data()


    assert data['messages'][str(channel1["channel_id"])]['messages'][1]['message'] == "hey"

    message_edit_v2(user2['token'], message_1, "yo")
    assert data['messages'][str(channel1["channel_id"])]['messages'][1]['message'] == "hey"

    # Success: if new message is empty string, delete message
    m_list_before_edit = channel_messages_v2(user3['token'], channel1["channel_id"], 0)
    assert len(m_list_before_edit['messages']) == 3

    message_edit_v2(user3['token'], message_2, "")
    m_list_after_edit = channel_messages_v2(user3['token'], channel1["channel_id"], 0)
    assert len(m_list_after_edit['messages']) == 2

    # InputError: message is more than 1000 characters
    with pytest.raises(InputError):
        message_edit_v2(user1['token'], message_0, "uh" * 1000)
    
    with pytest.raises(InputError):
        message_edit_v2(user2['token'], message_1, "um" * 510)
    
    # InputError: message_id refers to deleted message
    with pytest.raises(InputError):
        message_edit_v2(user3['token'], message_2, "deleted message")
    
    with pytest.raises(InputError):
        message_edit_v2(user1['token'], message_2, "owner edit deleted message")
    
    # AccessError: message edited by user who didn't send it and isn't owner of channel1
    with pytest.raises(AccessError):
        message_edit_v2(user3['token'], message_1, "didn't send message_1")
    
    with pytest.raises(AccessError):
        message_edit_v2(user2['token'], message_0, "didn't send message_0")
    

def test_message_share_v1():
    '''Testing message_share_v1() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Public channel_id: 1, 2
    channel1 = channels_create_v2(user1['token'], "test_channel_1", True)
    channel2 = channels_create_v2(user1['token'], "test_channel_2", True)

    # Add users to channel1 and channel2 and send messages
    channel_join_v2(user2['token'], channel1["channel_id"])
    message_channel1_0 = message_send_v2(user1['token'], channel1["channel_id"], "hey user2")
    message_channel1_1 = message_send_v2(user2['token'], channel1["channel_id"], "hi user1")

    channel_join_v2(user3['token'], channel2["channel_id"])
    message_send_v2(user1['token'], channel2["channel_id"], "hi user3")
    message_send_v2(user3['token'], channel2["channel_id"], "hello user1")

    # Create DMs and send messages
    dm01 = dm_create_v1(user1['token'], [user2['auth_user_id']])
    dm1 = dm01['dm_id']
    dm1_0 = message_senddm_v1(user1['token'], dm1, "hi user2")
    message_senddm_v1(user2['token'], dm1, "hey user1")

    dm02 = dm_create_v1(user1['token'], [user3['auth_user_id']])
    dm2 = dm02['dm_id']
    message_senddm_v1(user1['token'], dm2, "hello user3")
    dm2_1 = message_senddm_v1(user3['token'], dm2, "hey user1")

    # Success: message shared between channels
    m_list_before_share = channel_messages_v2(user1['token'], channel2["channel_id"], 0)
    assert len(m_list_before_share['messages']) == 2

    message_share_v1(user1['token'], message_channel1_0, "boom", channel2["channel_id"], -1)

    m_list_after_share = channel_messages_v2(user1['token'], channel2["channel_id"], 0)
    assert len(m_list_after_share['messages']) == 3

    # Success: message shared between DMs
    dm_before_share = dm_messages_v1(user1['token'], dm2, 0)
    assert len(dm_before_share['messages']) == 2

    message_share_v1(user1['token'], dm1_0, "idk", -1, dm2)

    dm_after_share = dm_messages_v1(user1['token'], dm2, 0)
    assert len(dm_after_share['messages']) == 3

    # Success: message shared from channel to DM
    c1_to_dm_before_share = dm_messages_v1(user1['token'], dm1, 0)
    assert len(c1_to_dm_before_share['messages']) == 2

    message_share_v1(user1['token'], message_channel1_1, "hi", -1, dm1)

    c1_to_dm_after_share = dm_messages_v1(user1['token'], dm1, 0)
    assert len(c1_to_dm_after_share['messages']) == 3

    # AccessError: authorised user hasn't joined channel/DM they are trying to share message to
    with pytest.raises(AccessError):
        message_share_v1(user2['token'], message_channel1_0, "nothing", channel2["channel_id"], -1) # Expect fail as user2 is not a member of channel2
    
    with pytest.raises(AccessError):
        message_share_v1(user3['token'], dm2_1, "message", -1, dm1) # Expect fail as user3 is not member of dm1


def test_message_senddm_v1():
    '''Testing message_senddm_v1() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Create DM for user1 and user2
    dm01 = dm_create_v1(user1['token'], user2['auth_user_id'])
    dm1 = dm01['dm_id']

    # Success: message sent 
    # dm_before_message = dm_messages_v1(user1['token'], dm1, 0)
    #assert len(dm_before_message['messages']) == 0

    message_senddm_v1(user1['token'], dm1, "hey user2")

    dm_after_message_1 = dm_messages_v1(user1['token'], dm1, 0)
    assert len(dm_after_message_1['messages']) == 1

    message_senddm_v1(user2['token'], dm1, "hello user1")

    dm_after_message_2 = dm_messages_v1(user1['token'], dm1, 0)
    assert len(dm_after_message_2['messages']) == 2

    # InputError: message is more than 1000 characters
    with pytest.raises(InputError):
        message_senddm_v1(user1['token'], dm1, "no" * 1000)
    
    with pytest.raises(InputError):
        message_senddm_v1(user2['token'], dm1, "long message" * 500)
    
    # AccessError: user is not member of DM
    with pytest.raises(AccessError):
        message_senddm_v1(user3['token'], dm1, "let me in")
    
    with pytest.raises(AccessError):
        message_senddm_v1(user3['token'], dm1, ":(")


def test_message_sendlater_v1():
    '''Testing message_sendlater_v1() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Public channel_id: 1, 2
    channel1 = channels_create_v2(user1['token'], "test_channel_1", True)
    channel2 = channels_create_v2(user1['token'], "test_channel_2", True)

    # Add users to channel1 and channel2
    channel_join_v2(user2['token'], channel1)

    message_sendlater_v1(user1['token'], channel1, "hello world", time.time() + 5)

    # InputError: invalid channel_id
    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], 20, "hello world", time.time() + 5)
    
    with pytest.raises(InputError):
        message_sendlater_v1(user2['token'], 30, "hey", time.time() + 5)

    # InputError: message is more than 1000 characters
    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], channel2, "hello" * 300, time.time() + 5)
    
    with pytest.raises(InputError):
        message_sendlater_v1(user2['token'], channel1, "hi" * 1000, time.time() + 5)

    # InputError: time sent is in the past
    with pytest.raises(InputError):
        message_sendlater_v1(user2['token'], channel1, "past", time.time() - 5)

    with pytest.raises(InputError):
        message_sendlater_v1(user1['token'], channel2, "message", time.time() - 5)

    # AccessError: authorised user hasn't joined channel they're trying to post to
    with pytest.raises(AccessError):
        message_sendlater_v1(user2['token'], channel2, "hi", time.time() + 5)
    
    with pytest.raises(AccessError):
        message_sendlater_v1(user3['token'], channel1, "hey", time.time() + 5) 


def test_sendlaterdm_v1():
    '''Testing message_sendlaterdm_v1() function'''
    clear_v1()

    # Create test users
    user1 = auth_register_v2("mail1@mail.com", "password", "First", "Last")
    user2 = auth_register_v2("mail2@mail.com", "password", "Second", "Last")
    user3 = auth_register_v2("mail3@mail.com", "password", "Third", "Last")

    # Create DM for user1 and user2 or user3
    dm02 = dm_create_v1(user1['token'], user2['auth_user_id'])
    dm2 = dm02['dm_id']

    dm03 = dm_create_v1(user1['token'], user3['auth_user_id'])
    dm3 = dm03['dm_id']

    message_sendlaterdm_v1(user1['token'], dm3, "hello user2", time.time() + 5)

    # InputError: invalid dm_id
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm2+20, "hello user2", time.time() + 5)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user2['token'], dm2+30, "invalid", time.time() + 5)

    # InputError: message more than 1000 characters
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user1['token'], dm2, "hello" * 1000, time.time() + 5)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user3['token'], dm3, "hi" * 600, time.time() + 5)

    # InputError: time sent is in the past
    with pytest.raises(InputError):
        message_sendlaterdm_v1(user2['token'], dm2, "hey", time.time() - 5)

    with pytest.raises(InputError):
        message_sendlaterdm_v1(user3['token'], dm3, "hello", time.time() - 5)

    # AccessError: authorised user is not member of DM
    with pytest.raises(AccessError):
        message_sendlaterdm_v1(user3['token'], dm2, "hi", time.time() + 5)

    with pytest.raises(AccessError):
        message_sendlaterdm_v1(user2['token'], dm3, "hey", time.time() + 5)


def test_message_pin_v1():
    clear_v1()
    # user1, user2 and user3 created
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    token1 = auth_user_id1["token"]
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    token2 = auth_user_id2["token"]
    auth_user_id3 = auth_register_v2('hilary@gmail.com','123456789','Hillary','Clinton')
    token3 = auth_user_id3["token"]

    # user1 creates a channel, adds user2 and sends a message
    chmsg = "Welcome george"
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channel_invite_v2(auth_user_id1['token'], channel_id1['channel_id'], auth_user_id2['auth_user_id'])
    msg1 = message_send_v2(auth_user_id1['token'], channel_id1['channel_id'], chmsg)
    
    # user1 created a new DM with user2 and sends a message
    dmmsg = "Hello George"
    newdm = dm_create_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'])
    msg2 = message_senddm_v1(auth_user_id1['token'], newdm['dm_id'], dmmsg)

    # trying to pin a msg with invalid msg id
    with pytest.raises(InputError):
        message_pin_v1(token1, 1234)

    # pinning channel message and dm message
    message_pin_v1(token1, msg1["message_id"])
    message_pin_v1(token1, msg2["message_id"])

    # trying to pin messages which are already pinned
    with pytest.raises(InputError):
        message_pin_v1(token1, msg1["message_id"])
    with pytest.raises(InputError):
        message_pin_v1(token1, msg2["message_id"])

    # unpinning messages
    message_unpin_v1(token1, msg1["message_id"])
    message_unpin_v1(token1, msg2["message_id"])

    # user that is not part of channel or dm trying to pin
    with pytest.raises(AccessError):
        message_pin_v1(token3, msg1["message_id"])
    with pytest.raises(AccessError):
        message_pin_v1(token3, msg2["message_id"])

    # user that is not owner of channel or dm trying to pin
    with pytest.raises(AccessError):
        message_pin_v1(token2, msg1["message_id"])
    with pytest.raises(AccessError):
        message_pin_v1(token2, msg2["message_id"])

    # pinning channel message and dm message
    message_pin_v1(token1, msg1["message_id"])
    message_pin_v1(token1, msg2["message_id"])

    # success channels message
    result = channel_messages_v2(token1,channel_id1["channel_id"], 0)
    assert result["messages"][0]["is_pinned"] == True
    
    # success dm message
    result = dm_messages_v1(token1,newdm["dm_id"], 0)
    assert result["messages"][0]["is_pinned"] == True

def test_message_unpin_v1():
    clear_v1()
    # user1, user2 and user3 created
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    token1 = auth_user_id1["token"]
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    token2 = auth_user_id2["token"]
    auth_user_id3 = auth_register_v2('hilary@gmail.com','123456789','Hillary','Clinton')
    token3 = auth_user_id3["token"]

    # user1 creates a channel, adds user2 and sends a message
    chmsg = "Welcome george"
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channel_invite_v2(auth_user_id1['token'], channel_id1['channel_id'], auth_user_id2['auth_user_id'])
    msg1 = message_send_v2(auth_user_id1['token'], channel_id1['channel_id'], chmsg)
    
    # user1 created a new DM with user2 and sends a message
    dmmsg = "Hello George"
    newdm = dm_create_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'])
    msg2 = message_senddm_v1(auth_user_id1['token'], newdm['dm_id'], dmmsg)
    
    # pinning channel message and dm message
    message_pin_v1(token1, msg1["message_id"])
    message_pin_v1(token1, msg2["message_id"])
    
    # trying to unpin a msg with invalid msg id
    with pytest.raises(InputError):
        message_unpin_v1(token1, 1234)

    # unpinning channel message and dm message
    message_unpin_v1(token1, msg1["message_id"])
    message_unpin_v1(token1, msg2["message_id"])

    # trying to unpin messages which are already pinned
    with pytest.raises(InputError):
        message_unpin_v1(token1, msg1["message_id"])
    with pytest.raises(InputError):
        message_unpin_v1(token1, msg2["message_id"])

    # pinning messages
    message_pin_v1(token1, msg1["message_id"])
    message_pin_v1(token1, msg2["message_id"])

    # user that is not part of channel or dm trying to unpin
    with pytest.raises(AccessError):
        message_unpin_v1(token3, msg1["message_id"])
    with pytest.raises(AccessError):
        message_unpin_v1(token3, msg2["message_id"])

    # user that is not owner of channel or dm trying to unpin
    with pytest.raises(AccessError):
        message_unpin_v1(token2, msg1["message_id"])
    with pytest.raises(AccessError):
        message_unpin_v1(token2, msg2["message_id"])

    # unpinning channel message and dm message
    message_unpin_v1(token1, msg1["message_id"])
    message_unpin_v1(token1, msg2["message_id"])

    # success channels message
    result = channel_messages_v2(token1,channel_id1["channel_id"], 0)
    assert result["messages"][0]["is_pinned"] == False
    
    # success dm message
    result = dm_messages_v1(token1,newdm["dm_id"], 0)
    assert result["messages"][0]["is_pinned"] == False

def test_message_react():
    clear_v1()
    data = load_data()
    # user1, user2 and user3 created
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    token1 = auth_user_id1["token"]
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    token2 = auth_user_id2["token"]
    auth_user_id3 = auth_register_v2('hilary@gmail.com','123456789','Hillary','Clinton')
    token3 = auth_user_id3["token"]

    # user1 creates a channel, adds user2 and sends a message
    chmsg = "Welcome George"
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channel_invite_v2(auth_user_id1['token'], channel_id1['channel_id'], auth_user_id2['auth_user_id'])
    msg1 = message_send_v2(auth_user_id2['token'], channel_id1['channel_id'], chmsg)
    
    # user1 created a new DM with user2 and sends a message
    dmmsg = "Hello George"
    newdm = dm_create_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'])
    msg2 = message_senddm_v1(auth_user_id2['token'], newdm['dm_id'], dmmsg)
    
    # input error with invalid messageid
    with pytest.raises(InputError):
        message_react_v1(token1, 1234, 1)

    # input error with invalid react id
    with pytest.raises(InputError):
        message_react_v1(token1, msg1["message_id"], 5)
    with pytest.raises(InputError):
        message_react_v1(token1, msg2["message_id"], 5)

    # user 1 reacts
    message_react_v1(token1, msg1["message_id"], 1)
    message_react_v1(token1, msg2["message_id"], 1)

    # input error when user 1 tries to react again to same msg
    with pytest.raises(InputError):
        message_react_v1(token1, msg1["message_id"], 1)
    with pytest.raises(InputError):
        message_react_v1(token1, msg2["message_id"], 1)

    # user3 trying to react
    with pytest.raises(AccessError):
        message_react_v1(token3, msg1["message_id"], 1)
    with pytest.raises(AccessError):
        message_react_v1(token3, msg2["message_id"], 1)
    data  = load_data()
    expectedoutput = {'messages':
        [
            {
                "message_id": msg2['message_id'],
                'u_id':auth_user_id2['auth_user_id'],
                'message': dmmsg,
                'time_created':data["dm_messages"][str(newdm['dm_id'])]['messages'][0]['time_created'],
                'is_pinned': False,
                'reacts':[auth_user_id1["auth_user_id"]]
            },
            {
                "message_id": msg1['message_id'],
                'u_id':auth_user_id2['auth_user_id'],
                'message': chmsg,
                'time_created': data["messages"][str(channel_id1['channel_id'])]['messages'][0]['time_created'],
                'is_pinned': False,
                'reacts':[auth_user_id1["auth_user_id"]]
            }
        ]
    }

    assert search_v1(token2, "George") == expectedoutput

def test_message_unreact():
    clear_v1()
    # user1, user2 and user3 created
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    token1 = auth_user_id1["token"]
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    auth_user_id3 = auth_register_v2('hilary@gmail.com','123456789','Hillary','Clinton')
    token3 = auth_user_id3["token"]

    # user1 creates a channel, adds user2 and sends a message
    chmsg = "Welcome george"
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channel_invite_v2(auth_user_id1['token'], channel_id1['channel_id'], auth_user_id2['auth_user_id'])
    msg1 = message_send_v2(auth_user_id2['token'], channel_id1['channel_id'], chmsg)
    
    # user1 created a new DM with user2 and sends a message
    dmmsg = "Hello George"
    newdm = dm_create_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'])
    msg2 = message_senddm_v1(auth_user_id2['token'], newdm['dm_id'], dmmsg)

    # user 1 reacts
    message_react_v1(token1, msg1["message_id"], 1)
    message_react_v1(token1, msg2["message_id"], 1)

    # input error with invalid messageid
    with pytest.raises(InputError):
        message_unreact_v1(token1, 1234, 1)

    # input error with invalid react id
    with pytest.raises(InputError):
        message_unreact_v1(token1, msg1["message_id"], 5)
    with pytest.raises(InputError):
        message_unreact_v1(token1, msg2["message_id"], 5)

    # user 1 unreacts
    message_unreact_v1(token1, msg1["message_id"], 1)
    message_unreact_v1(token1, msg2["message_id"], 1)

    # input error when user 1 tries to unreact again to same msg
    with pytest.raises(InputError):
        message_unreact_v1(token1, msg1["message_id"], 1)
    with pytest.raises(InputError):
        message_unreact_v1(token1, msg2["message_id"], 1)

    # user3 trying to unreact
    with pytest.raises(AccessError):
        message_unreact_v1(token3, msg1["message_id"], 1)
    with pytest.raises(AccessError):
        message_unreact_v1(token3, msg2["message_id"], 1)
