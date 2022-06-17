import requests 
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2, channels_listall_v2
from src.error import AccessError
from src.utils import token_to_id
from src.utils import token_to_id

url = "http://127.0.0.1:8080/"

def test_channel_list_v1():
    """Testing basic functionality of channel_list when a single user has joined a single channel"""
    clear_v1()
    #Register new user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]
    
    # list channels 
    expected_output = {
        'channels': [
            {
                'channel_id': channel_id1,
                'name':'Testing Channel'
            }
        ]
    }
    r = requests.get(f"{url}/channels/list/v2", json={
        "token": token1,
    })
    payload = r.json()

    assert payload == expected_output

def test_channel_list_multiple():
    """Testing that channel_list correctly lists channels that user has joined when number of channels > 1."""
    clear_v1()
    #Register new user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel2",
        "is_public": True
    })
    payload = r.json()
    channel_id2 = payload["channel_id"]
    
    # list channels 
    expected_output = {
        'channels': [
            {
                'channel_id': channel_id1,
                'name':'Testing Channel'
            },
            {
                'channel_id': channel_id2,
                'name':'Testing Channel2'
            }
        ]
    }
    r = requests.get(f"{url}/channels/list/v2", json={
        "token": token1,
    })
    payload = r.json()

    assert payload == expected_output


def test_channel_list_no_channels():
    """User not part of any channels"""
    clear_v1()
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # list channels
    r = requests.get(f"{url}/channels/list/v2", json={
        "token": token1,
    })
    payload = r.json()
    
    assert payload == {'channels':[]}


def test_channels_list_created_or_invited():
    """Testing that list of channels shows all channels created by the user as well as channels the user has been invited to by other users"""
    clear_v1()
    # register 2 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]
    u_id2 = payload["auth_user_id"]

    # create channels
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel1",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Testing Channel2",
        "is_public": True
    })
    payload = r.json()
    channel_id2 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Testing Channel3",
        "is_public": True
    })
    payload = r.json()
    channel_id3 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Testing Channel4",
        "is_public": True
    })
    payload = r.json()
    channel_id4 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Testing Channel5",
        "is_public": True
    })
    payload = r.json()
    channel_id5 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token2,
        "name": "Testing Channel6",
        "is_public": True
    })
    payload = r.json()
    channel_id6 = payload["channel_id"]

    #Adding all channels to data
    expectedoutput = {
        'channels': [
            {'channel_id':channel_id1,'name':'Testing Channel1'},
            {'channel_id':channel_id2,'name':'Testing Channel2'},
            {'channel_id':channel_id3,'name':'Testing Channel3'},
            {'channel_id':channel_id4,'name':'Testing Channel4'},
            {'channel_id':channel_id5,'name':'Testing Channel5'},
            {'channel_id':channel_id6,'name':'Testing Channel6'}
        ]
    }

    #User 1 invites user 2 to their channel
    r = requests.post(f"{url}/channel/invite/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "u_id": u_id2
    })
    payload = r.json()

    #User 2 (auth_user_id2) should now be part of all 6 channels
    # list
    r = requests.get(f"{url}/channels/list/v2", json={
        "token": token2,
    })
    payload = r.json()
    
    assert payload == expectedoutput

def test_channels_listall_v1_empty():
    """Test functions for channels_listall_v1"""
    #No Channels, valid auth_user_id
    clear_v1()
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # listall channels
    r = requests.get(f"{url}/channels/listall/v2", json={
        "token": token1,
    })
    payload = r.json()
    
    assert payload == {'channels':[]}

def test_channels_listall_v1_single():
    """Listing all channels when only one channel has been created"""
    clear_v1()
    #Register new user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]
    
    # list channels 
    expected_output = {
        'channels': [
            {
                'channel_id': channel_id1,
                'name':'Testing Channel'
            }
        ]
    }
    r = requests.get(f"{url}/channels/listall/v2", json={
        "token": token1,
    })
    payload = r.json()

    assert payload == expected_output
    clear_v1()

def test_channels_listall_v1_multiple():
    """Listing all channels when multiple channels have been created"""
    clear_v1()
    #Register new user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel2",
        "is_public": True
    })
    payload = r.json()
    channel_id2 = payload["channel_id"]
    
    # list channels 
    expected_output = {
        'channels': [
            {
                'channel_id': channel_id1,
                'name':'Testing Channel'
            },
            {
                'channel_id': channel_id2,
                'name':'Testing Channel2'
            }
        ]
    }
    r = requests.get(f"{url}/channels/listall/v2", json={
        "token": token1,
    })
    payload = r.json()

    assert payload == expected_output
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
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "camila",
        "name_last": "moro"
    })
    payload = r.json()
    token1 = payload["token"]
    u_id1 = payload["auth_user_id"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Camilas Channel",
        "is_public": False
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # channel details
    r = requests.get(f"{url}/channel/details/v2", json={
        "token": token1,
        "channel_id": channel_id1,
    })
    payload = r.json()

    expected_output = {
        'name': 'Camilas Channel',
        'owner_members': [{'email':'camila@gmail.com', 'name_first':'camila','name_last':'moro', 'handle_str':'camilamoro','u_id': u_id1}],
        'all_members': [{'email':'camila@gmail.com', 'name_first':'camila','name_last':'moro', 'handle_str':'camilamoro','u_id': u_id1}]
    }
    assert expected_output == payload

def test_channels_create_private_v1():
    """Test function for channels_create_v2 - creating a private channel"""
    clear_v1()
    #Registering a new user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "camila",
        "name_last": "moro"
    })
    payload = r.json()
    token1 = payload["token"]
    u_id1 = payload["auth_user_id"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Private Channel",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]

    # channel details
    r = requests.get(f"{url}/channel/details/v2", json={
        "token": token1,
        "channel_id": channel_id1,
    })
    payload = r.json()

    expected_output = {
        'name': 'Private Channel',
        'owner_members': [{'email':'camila@gmail.com', 'name_first':'camila','name_last':'moro', 'handle_str':'camilamoro','u_id': u_id1}],
        'all_members': [{'email':'camila@gmail.com', 'name_first':'camila','name_last':'moro', 'handle_str':'camilamoro','u_id': u_id1}]
    }
    assert expected_output == payload
    
def test_channels_create_v2_errors2():
    """Test function for channels_create_v2 - error raising scenarios"""
    clear_v1()
    #Registering a new user
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "camila",
        "name_last": "moro"
    })
    payload = r.json()
    token1 = payload["token"]

    # create channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Camilas very long channel name that is too long",
        "is_public": True
    })
    payload = r.json()
    
    assert payload["name"] == "System Error"

def test_channel_create_invite_list():
    """Testing that a user is able create a channel and invite another user then both of their lists match"""
    clear_v1()

    # register 2 users
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "camila@gmail.com",
        "password": "123456789",
        "name_first": "Camila",
        "name_last": "Moro"
    })
    payload = r.json()
    token1 = payload["token"]

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "george@gmail.com",
        "password": "123456789",
        "name_first": "George",
        "name_last": "Bush"
    })
    payload = r.json()
    token2 = payload["token"]

    u_id2 = token_to_id(token2)

    # create a channel
    r = requests.post(f"{url}/channels/create/v2", json={
        "token": token1,
        "name": "Testing Channel1",
        "is_public": True
    })
    payload = r.json()
    channel_id1 = payload["channel_id"]


    #Invite user 2 to channel
    r = requests.post(f"{url}/channel/invite/v2", json={
        "token": token1,
        "channel_id": channel_id1,
        "u_id": u_id2
    })
    payload = r.json()

    # list
    r = requests.get(f"{url}/channels/list/v2", json={
        "token": token1,
    })
    payload1 = r.json()

    r = requests.get(f"{url}/channels/list/v2", json={
        "token": token2,
    })
    payload2 = r.json()
    
    assert payload1 == payload2
