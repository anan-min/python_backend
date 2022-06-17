import pytest

from src.other import clear_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.channel import channel_details_v2, channel_invite_v2
from src.error import InputError, AccessError
from src.data import channels
from src.admin import admin_user_remove_v1, admin_user_permission_change_v1
from src.user import user_profile_v2
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_senddm_v1
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.utils import load_data

def test_admin_user_permission():
    #Creating three users
    clear_v1()
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    auth_user_id3 = auth_register_v2('thirduser@hotmail.com', 'abcdefghi', 'Third', 'User')

    #User2 (not owner) tying to make user3 an owner
    with pytest.raises(AccessError):
        admin_user_permission_change_v1(auth_user_id2['token'], auth_user_id3['auth_user_id'], 1)
    
    #Trying to add owner using invalid u_id
    with pytest.raises(InputError):
        admin_user_permission_change_v1(auth_user_id1['token'], 999999999, 1)

    #User1 making user2 and user3 an owener
    admin_user_permission_change_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'], 1)
    admin_user_permission_change_v1(auth_user_id1['token'], auth_user_id3['auth_user_id'], 1)

    #User2 making user1 a member only then removing them from Dreams
    admin_user_permission_change_v1(auth_user_id2['token'], auth_user_id1['auth_user_id'], 2)
    admin_user_remove_v1(auth_user_id2['token'], auth_user_id1['auth_user_id'])
    profile = user_profile_v2(auth_user_id2['token'],  auth_user_id1['auth_user_id'])
    assert profile['name_first'] == 'Removed'

def test_admin_remove():
    clear_v1()
    #Creating two users 
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    
    #User2 sends message to user1
    msg = "Message"
    data = load_data()
    print(data["users"])
    newdm = dm_create_v1(auth_user_id2['token'], [auth_user_id1['auth_user_id']])
    message_senddm_v1(auth_user_id2['token'], newdm['dm_id'], msg)

    #Trying to remove a user with invalid user id
    with pytest.raises(InputError):
        admin_user_remove_v1(auth_user_id1['token'], 'hello')
    with pytest.raises(InputError):
        admin_user_remove_v1(auth_user_id1['token'], 999999999)

    #User1 removes user2
    admin_user_remove_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'])

    #Checking if removal has been successful
    profile = user_profile_v2(auth_user_id1['token'],  auth_user_id2['auth_user_id'])
    dm_messages_v1(auth_user_id1['token'], newdm['dm_id'],0)
    assert profile['name_first'] == 'Removed'
    # this is a list of message
    #assert message['messages'] == 'Removed user'
    

    #Creating user2 again # caused eror in register due to repeat register the same user
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')

    #User2 trying to remove user1 (owner of dreams)
    with pytest.raises(AccessError):
        admin_user_remove_v1(auth_user_id2['token'], auth_user_id1['auth_user_id'])

    #User1 trying to remove themselves
    with pytest.raises(InputError):
        admin_user_remove_v1(auth_user_id1['token'], auth_user_id1['auth_user_id'])

def test_camila():
    r1 = auth_register_v2("test1@gmail.com","nut12bodin","aa","aa")
    auth_register_v2("test2@gmail.com","nut12bodin","aa","aa")
    channels_create_v2(r1["token"], "Private Channel", True)
