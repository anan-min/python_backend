"""Importing functions and variables"""
import pytest
from src.utils import load_data, token_to_id
from src.auth import auth_register_v2, auth_login_v2
from src.other import clear_v1, search_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.channel import channel_details_v2, channel_invite_v2
from src.error import InputError
from src.message import message_send_v2, message_senddm_v1
from src.dm import dm_create_v1
from src.data import users, channels, messages, dmmessages

#Test functions for clear_v1
def test_clear_v1_simple():
    """Clears all previous data allowing only new data entered after clear_v1()
    to be called"""
    clear_v1()
    #New user created and 5 channels created by that user
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channels_create_v2(auth_user_id1['token'], 'Another Channel',True)
    channels_create_v2(auth_user_id1['token'], 'Public Channel',False)
    channels_create_v2(auth_user_id1['token'], 'Some Channel',False)
    channels_create_v2(auth_user_id1['token'], 'Last Channel',True)
    #clear
    clear_v1()
    #New(different) user and channel(different) created by that user
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    channel_id2 = channels_create_v2(auth_user_id2['token'], 'Georges Channel',True)
    allchannels = channels_listall_v2(auth_user_id2['token'])
    expectedoutput = {
						'channels':
							[
								{'channel_id':channel_id2["channel_id"],'name':'Georges Channel'}
							]
					}
    assert allchannels == expectedoutput

def test_clear_v1_errors():
    """Scenarios which raise an error"""
    clear_v1()
    #New user created
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    #Clear
    clear_v1()
    #Trying to log in with cleared user credentials
    with pytest.raises(InputError):
        auth_login_v2('camila@gmail.com','123456789')

    #Creating a user
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    #Clear
    clear_v1()
    #Creating a different user and new channel and then trying to invite previous
    #(cleared) user to join
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    channel_id2 = channels_create_v2(auth_user_id2['token'], 'Georges Channel',True)
    with pytest.raises(InputError):
        channel_invite_v2(auth_user_id2['token'],channel_id2['channel_id'],auth_user_id1['auth_user_id'])

    clear_v1()
    #Creating a user and channel
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    #Clear
    clear_v1()
    #Creating user again
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    #Trying to pull details about cleared channel
    with pytest.raises(InputError):
        channel_details_v2(auth_user_id1['token'],channel_id1['channel_id'])

def test_search_nomessages():
    clear_v1()
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    assert search_v1(auth_user_id1['token'], 'message') == {'messages':[]}

def test_search_onedm():
    clear_v1()
    # can't fix  the error is due to time_created  ? where is messages initialize
    msg = "This is a message"
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    newdm = dm_create_v1(auth_user_id1['token'], [auth_user_id2['auth_user_id']])
    sentdm = message_senddm_v1(auth_user_id1['token'], newdm['dm_id'], msg)
    strng = 'This is a message'
    data = load_data()
    assert search_v1(auth_user_id2['token'], strng) == {'messages':
        [
            {
                "message_id": sentdm['message_id'],
                'u_id':auth_user_id1['auth_user_id'],
                'message': msg,
                'time_created':data["dm_messages"][str(newdm['dm_id'])]['messages'][0]['time_created'],
                'is_pinned': False,
                'reacts':[]
            }
        ]
    }

def test_onemessage():
    clear_v1()
    msg = "This is a message"
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    sentmessage = message_send_v2(auth_user_id1['token'], channel_id1['channel_id'], msg)
    data = load_data()
    assert search_v1(auth_user_id1['token'], msg) == {"messages": [{
        'message_id': sentmessage['message_id'],
        'u_id':auth_user_id1['auth_user_id'],
        'message': msg,
        'time_created': data["messages"][str(channel_id1["channel_id"])]["messages"][0]["time_created"],
        'is_pinned': False,
        'reacts':[]
        }]
    }

def test_multipledm():
    clear_v1()

    msg = "This is a message"
    msg2 = 'This is also a message'
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    auth_user_id3 = auth_register_v2('adam@gmail.com','123456789','Adam','Eve')
    newdm = dm_create_v1(auth_user_id1['token'], [auth_user_id2['auth_user_id']])
    sentdm1 = message_senddm_v1(auth_user_id1['token'], newdm['dm_id'], msg)
    newdm2 = dm_create_v1(auth_user_id2['token'], [auth_user_id3['auth_user_id']])
    sentdm2 = message_senddm_v1(auth_user_id2['token'], newdm2['dm_id'], msg2)
    strng = 'message'
    data = load_data()
    expectedoutput = {'messages':[
        {'message_id': sentdm1['message_id'],
        'u_id':auth_user_id1['auth_user_id'],
        'message': msg,
        'time_created':data["dm_messages"][str(newdm['dm_id'])]['messages'][0]['time_created'],
        'is_pinned': False,
        'reacts':[]},
        {'message_id': sentdm2['message_id'],
        'u_id':auth_user_id2['auth_user_id'],
        'message': msg2,
        'time_created':data["dm_messages"][str(newdm2['dm_id'])]['messages'][0]['time_created'],
        'is_pinned': False,
        'reacts':[]}
        ]}
    assert search_v1(auth_user_id2['token'], strng) == expectedoutput

def test_multiplemessages():
    clear_v1()
    data = load_data()
    msg = "This is a message"
    msg2 = 'Another message'
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    sentmessage = message_send_v2(auth_user_id1['token'], channel_id1['channel_id'], msg)
    channel_id2 = channels_create_v2(auth_user_id2['token'], 'George Channel',True)
    channel_invite_v2(auth_user_id2['token'], channel_id2['channel_id'], auth_user_id1['auth_user_id'])
    sentmessage2 = message_send_v2(auth_user_id2['token'], channel_id2['channel_id'], msg2)
    data  = load_data()
    expectedoutput ={'messages': [
        {'message_id': sentmessage['message_id'],
        'u_id':auth_user_id1['auth_user_id'],
        'message': msg,
        'time_created':data["messages"][str(channel_id1['channel_id'])]['messages'][0]['time_created'],
        'is_pinned': False,
        'reacts':[]},
        {'message_id': sentmessage2['message_id'],
        'u_id':auth_user_id2['auth_user_id'],
        'message': msg2,
        'time_created':data["messages"][str(channel_id2['channel_id'])]['messages'][0]['time_created'],
        'is_pinned': False,
        'reacts':[]}]}
    assert search_v1(auth_user_id1['token'], 'message') == expectedoutput

def test_dmandmessages():
    clear_v1()
    msg = "This is a message"
    msg2 = 'Another message'
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    newdm = dm_create_v1(auth_user_id1['token'], [auth_user_id2['auth_user_id']])
    sentdm1 = message_senddm_v1(auth_user_id1['token'], newdm['dm_id'], msg)
    channel_id2 = channels_create_v2(auth_user_id2['token'], 'George Channel',True)
    sentmessage2 = message_send_v2(auth_user_id2['token'], channel_id2['channel_id'], msg2)
    data = load_data()
    expectedoutput = {'messages': 
        [
            {'message_id': sentdm1['message_id'],
            'u_id':int(token_to_id(auth_user_id1['token'])),
            'message': msg,
            'time_created':data["dm_messages"][str(newdm['dm_id'])]['messages'][0]['time_created'],
            'is_pinned': False,
            'reacts':[]},
            {'message_id': sentmessage2['message_id'],
            'u_id':int(token_to_id(auth_user_id2['token'])),
            'message': msg2,
            'time_created': data["messages"][str(channel_id2['channel_id'])]['messages'][0]['time_created'],
            'is_pinned': False,
            'reacts':[]}
        ]
    }
    assert search_v1(auth_user_id2['token'], 'message') == expectedoutput

def test_search_error():
    clear_v1()
    strng = 'i' * 20000
    strng2 = 'i' * 1001
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    with pytest.raises(InputError):
        search_v1(auth_user_id1['token'], strng)
    with pytest.raises(InputError):
        search_v1(auth_user_id1['token'], strng2)
