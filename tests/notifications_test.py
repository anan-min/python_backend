"""Importing functions and variables"""
from src.auth import auth_register_v2, auth_login_v2
from src.other import clear_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.channel import channel_details_v2, channel_invite_v2
from src.error import InputError
from src.notifications import notifications_get_v1
from src.message import message_send_v2, message_senddm_v1
from src.dm import dm_create_v1

def test_get():
    clear_v1()
    #Creating two users
    auth_user_id1 = auth_register_v2('camila@gmail.com','123456789','Camila','Moro')
    auth_user_id2 = auth_register_v2('george@gmail.com','123456789','George','Bush')
    #User one creates a channel and adds user2
    channel_id1 = channels_create_v2(auth_user_id1['token'], 'Private Channel',True)
    channel_invite_v2(auth_user_id1['token'], channel_id1['channel_id'], auth_user_id2['auth_user_id'])
    message_send_v2(auth_user_id1['token'], channel_id1['channel_id'], "Welcome @georgebush")
    #User one created a new DM with user 2 and sends a message
    msg = "Hello @georgebush"
    newdm = dm_create_v1(auth_user_id1['token'], auth_user_id2['auth_user_id'])
    message_senddm_v1(auth_user_id1['token'], newdm['dm_id'], msg)
    #Expected output
    notificationsoutput = {"notifications":
    [
        {
            'channel_id': -1, 
            'dm_id': int(newdm['dm_id']),
            'notification_message' : "camilamoro tagged you in camilamoro, georgebush: Hello @georgebush"
        },
        {
            'channel_id': -1, 
            'dm_id': int(newdm['dm_id']),
            'notification_message' : "camilamoro added you to camilamoro, georgebush"
        },
        {
            'channel_id': int(channel_id1['channel_id']), 
            'dm_id': -1,
            'notification_message' : "camilamoro tagged you in Private Channel: Welcome @georgebush"
        },
        {
            'channel_id': int(channel_id1['channel_id']), 
            'dm_id': -1,
            'notification_message' : "camilamoro added you to Private Channel"
        },
    ]}
    assert notificationsoutput == notifications_get_v1(auth_user_id2['token'])
