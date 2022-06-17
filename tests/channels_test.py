"""Importing functions"""
import pytest
from src.auth import auth_register_v2
from src.other import clear_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.channel import channel_details_v2, channel_invite_v2
from src.error import InputError, AccessError
from src.data import channels


def test_channel_list_v1():
    """Testing basic functionality of channel_list when a single user has joined a single channel"""
    clear_v1()
    #Register new user
    auth_user_id1 = auth_register_v2('alex@gmail.com','securepassw0rd1','Alex','Culic')
    new_channel = channels_create_v2(auth_user_id1['token'], 'Testing Channel', True)
    expected_output = {
        'channels': [
            {
                'channel_id': new_channel['channel_id'],
                'name':'Testing Channel'
            }
        ]
    }
    assert  channels_list_v2(auth_user_id1['token']) == expected_output

def test_channel_list_multiple():
    """Testing that channel_list correctly lists channels that user has joined when number of channels > 1."""
    clear_v1()
    #Register new user
    auth_user_id1 = auth_register_v2('alex@gmail.com', 's3cur3p@ssw0rD', 'Alex', 'Culic')
    newchannel1 = channels_create_v2(auth_user_id1['token'], 'Testing Channel 1', True)
    newchannel2 = channels_create_v2(auth_user_id1['token'], 'Testing Channel 2', True)
    expected_output = {
        'channels': [
            {'channel_id':newchannel1['channel_id'],'name':'Testing Channel 1'},
            {'channel_id':newchannel2['channel_id'],'name':'Testing Channel 2'}
        ]
    }
    assert channels_list_v2(auth_user_id1['token']) == expected_output


def test_channel_list_no_channels():
    """User not part of any channels"""
    clear_v1()
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    #User should not be part of any channels
    assert channels_list_v2(auth_user_id1['token']) == {'channels':[]}


def test_channels_list_created_or_invited():
    """Testing that list of channels shows all channels created by the user as well as channels the user has been invited to by other users"""
    clear_v1()
    auth_user_id1 = auth_register_v2('alex@gmail.com','securepassw0rd1','Alex','Culic')
    auth_user_id2 = auth_register_v2('camila@gmail.com','password556', 'Camila', 'Moro')

    #Users both create channels (user 2 creates 5, user 1 creates 1)
    newchannel1 = channels_create_v2(auth_user_id1['token'],"Testing Channel1", True)
    newchannel2 = channels_create_v2(auth_user_id2['token'],"Testing Channel2", True)
    newchannel3 = channels_create_v2(auth_user_id2['token'],"Testing Channel3", True)
    newchannel4 = channels_create_v2(auth_user_id2['token'],"Testing Channel4", True)
    newchannel5 = channels_create_v2(auth_user_id2['token'],"Testing Channel5", True)
    newchannel6 = channels_create_v2(auth_user_id2['token'],"Testing Channel6", True)

    #Adding all channels to data
    expectedoutput = {
        'channels': [
            {'channel_id':newchannel1['channel_id'],'name':'Testing Channel1'},
            {'channel_id':newchannel2['channel_id'],'name':'Testing Channel2'},
            {'channel_id':newchannel3['channel_id'],'name':'Testing Channel3'},
            {'channel_id':newchannel4['channel_id'],'name':'Testing Channel4'},
            {'channel_id':newchannel5['channel_id'],'name':'Testing Channel5'},
            {'channel_id':newchannel6['channel_id'],'name':'Testing Channel6'}
        ]
    }

    #User 1 invites user 2 to their channel
    channel_invite_v2(auth_user_id1['token'], newchannel1['channel_id'], auth_user_id2['auth_user_id'])

    #User 2 (auth_user_id2) should now be part of all 6 channels
    assert channels_list_v2(auth_user_id2['token']) == expectedoutput
'''
def test_channels_listall_v2_empty():
    """Test functions for channels_listall_v2"""
    #No Channels, valid auth_user_id
    clear_v1()
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    all_channels = channels_listall_v2(auth_user_id1['token'])
    expected_output = {'channels': []}
    assert all_channels == expected_output

def test_channels_listall_v2_single():
    """Listing all channels when only one channel has been created"""
    clear_v1()
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    all_channels = channels_listall_v2(auth_user_id1['token'])
    expected_output = {'channels':[{'channel_id':channel_id1['channel_id'],'name':'Private Channel'}]}
    assert all_channels == expected_output

def test_channels_listall_v2_multiple():
    """Listing all channels when multiple channels have been created"""
    clear_v1()
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channel_id2 = channels_create_v2(auth_user_id1['token'], 'Another Channel',True)
    channel_id3 = channels_create_v2(auth_user_id1['token'], 'Public Channel',False)
    channel_id4 = channels_create_v2(auth_user_id1['token'], 'Some Channel',False)
    channel_id5 = channels_create_v2(auth_user_id1['token'], 'Last Channel',True)
    allchannels = channels_listall_v2(auth_user_id1['token'])
    expectedoutput = {
        'channels': [
            {'channel_id':channel_id1['channel_id'],'name':'Private Channel'},
            {'channel_id':channel_id2['channel_id'],'name':'Another Channel'},
            {'channel_id':channel_id3['channel_id'],'name':'Public Channel'},
            {'channel_id':channel_id4['channel_id'],'name':'Some Channel'},
            {'channel_id':channel_id5['channel_id'],'name':'Last Channel'}
        ]
    }
    assert allchannels == expectedoutput

def test_channels_create_public_v1():
    """Test function for channels_create_v2 - creating a public channel"""
    clear_v1()
    #Registering a new user
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')

    #Creating a new public channel and looking at channel details
    channel_id1 = channels_create_v2(auth_user_id1['token'],'Camilas Channel', False)
    channel_details = channel_details_v2(auth_user_id1['token'],channel_id1['channel_id'])
    expected_output = {
        'name': 'Camilas Channel',
        'owner_members': [{'email':'camila@gmail.com', 'name_first':'Camila','name_last':'Moro', 'handle_str':'camilamoro','u_id': auth_user_id1['auth_user_id']}],
        'all_members': [{'email':'camila@gmail.com', 'name_first':'Camila','name_last':'Moro', 'handle_str':'camilamoro','u_id': auth_user_id1['auth_user_id']}]
    }
    assert expected_output == channel_details

    #Trying to create a duplicate channel, will create another channel 
    #with same name but different id
    channel_id2 = channels_create_v2(auth_user_id1['auth_user_id'],'Camilas Channel', False)

    assert channel_id2 != channel_id1

def test_channels_create_private_v1():
    """Test function for channels_create_v2 - creating a private channel"""
    clear_v1()
    #Registering a new user
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')

    #Creating a new private channel
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel', True)
    channeldetails = channel_details_v2(auth_user_id1['token'],channel_id1['channel_id'])
    expectedoutput = {
        'name': 'Private Channel',
        'owner_members': [{'email':'camila@gmail.com', 'name_first':'Camila','name_last':'Moro', 'handle_str':'camilamoro','u_id': auth_user_id1['auth_user_id']}],
        'all_members': [{'email':'camila@gmail.com', 'name_first':'Camila','name_last':'Moro', 'handle_str':'camilamoro','u_id': auth_user_id1['auth_user_id']}]
    }
    assert expectedoutput == channeldetails

def test_channels_create_v2_errors2():
    """Test function for channels_create_v2 - error raising scenarios"""
    clear_v1()
    #Registering a new user
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')

    #Creating a channel with a name that is too long (more than
    #20 characters)

    with pytest.raises(InputError):
        channels_create_v2(auth_user_id1['token'], 'Camilas Very Long Channel Name', True)

def test_channel_create_invite_list():
    """Testing that a user is able create a channel and invite another user then both of their lists match"""
    clear_v1()

    #Register two new users
    auth_user_id1 = auth_register_v2('alex@gmail.com','securepassw0rd1','Alex','Culic')
    auth_user_id2 = auth_register_v2('camila@gmail.com','password556', 'Camila', 'Moro')

    #User one create channel
    newchannel = channels_create_v2(auth_user_id1['token'],"Testing Channel", True)

    #Invite user 2 to channel
    channel_invite_v2(auth_user_id1['token'], newchannel['channel_id'], auth_user_id2['auth_user_id'])

    #Test channels_list_v2
    assert channels_list_v2(auth_user_id1['token']) == channels_list_v2(auth_user_id2['token'])
'''
