    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 10:05:51 2021

@author: z5218628
"""

users = {}
"""
     format:
        dictionary containing dictionaries where key = user id and value is dictionary with user info
        
    {
        
            "u_id": {
                "email":, 
                "password":,
                "name_first":,
                "name_last":,
                "session_ids": [],
                "reset_code": 
            },
            "u_id": {
                "email":, 
                "password":, 
                "name_first":,
                "name_last":,
                "handle_str":
                "permission_id":,
                "reset_code":
            },
       
       
    }



"""
channels = {}
"""
    format:
        dictionary containing list of dictornaries where each dictionary 
        contains channel_id, name
        
    {
         'channels': [
             {
                "channel_id":, 
                "name":,
                "is_public": (True or False),
                "is_active": (True or False),
                "owner_members":[list with user ids],
                "all_members": [list with user ids]
            }
         ]
    }

"""

channel_info = {}
"""
    format:
        dictionary containing list of dictionaries where each dictionary contains 
        channel_name, channel_owners, all_members
    {
        channel_id:
        {
            'name': 'Hayden',
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
        },
        channel_id2:
        {
            'name': 'Hayden',
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
        }
    } 
"""
channel_standup = {}
"""
{
	"1000": {
		"is_active": "False",
		"time_finish": "None",
		"length": "0",
        "buffered_list": []
	},
	"1001": {
		"is_active": "False",
		"time_finish": "None",
		"length": "0",
        "buffered_list": []
	}
}
"1000" and "1001" is channel id.
"is_active" is boolean
"time_finish": initilly will be str none, but when stand up is active this will be an int in python
length is int in python by default 0
this data structure will be create when channl is created(inside channel_create function)
"""
messages = {}
'''
{
    channel_id:
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'total': num_total_messages
        },
    channel_id2:
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'total': num_total_messages
        }
}
'''
dmmessages = {}
'''
{
    dm_id1:
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'total': num_total_messages
        },
    dm_id2:
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
}
'''
dm_messages = {}
'''
{
    dm_id1:
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'total': num_total_messages
        },
    dm_id2:
        {
            'messages': [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
            ],
            'start': 0,
            'end': 50,
        }
}
'''
dms = {}
'''
   {
       dm_id1: {
            dm_id: DMID1,
            'creator': auth_id,
            name: DMname,
            members: [auth_id1,auth_id2],
            },
        dm_id2: {
            dm_id: DMID2,
            'creator': auth_id,
            name: DMname, 
            members: [auth_id1,auth_id2],
            }
    }
'''
notifications = {}
'''
List of dictionaries where each dictionary contains types
{channel_id, dm_id, notification_message}
channel_id = id of channel that the event happened in or -1 if being sent to a dm
dm_id = DM that the event happened in and is -1 if it is being sent to a channel
List should be ordered from most to least recent
Notification_message = string of following format for each trigger action:
    - tagged = "{users handle} tagged you in {Channel/dm message}: {first 20 characters of the message}
    - added to a channel/DM: "{users handle} added you to {channel/DM name}

notifications = {
    'auth_id': [
        {
            channel_id; 5,
            dm_id: -1,
            notification_message: "camilamoro tagged you in Camilas Channel: Hello!"
        }, 
        {
            channel_id; 5,
            dm_id: -1,
            notification_message: "camilamoro added you to Camilas Channel"
        }
    ],
    'auth_id': [
        {
            channel_id; 5,
            dm_id: -1,
            notification_message: "camilamoro tagged you in Camilas Channel: Hello!"
        }, 
        {
            channel_id; 5,
            dm_id: -1,
            notification_message: "camilamoro added you to Camilas Channel"
        }
    ]
}
'''
