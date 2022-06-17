# Assumptions File

## Global assumptions
1. Private class declaration: Due to a lack of explicit 'private' functions in python, functions prefixed with a double underscore '__' have been treated as private. 
2. There will not be more than 999 channels in Dreams

## auth.py
    1. During coding, we dicided to store all data into a separate file called data.py. And we diceided to use nested dictionary to store users information. The main dictionary contains all auth_user_id as key and users information as value. And for each sub-dictionary, key would be information type, like email address, names and password, corresponding values will be user's persoal detail. With this format, we will be able to access the data efficiently.
    2. To begin with, we though the term 'handle' stands for the same meanning as auth_user_id. So we wrote tests returning string with 'auth_user_id' instead of integer. But we fixed this problem in the end.
    3. We did some comments poorly. Foe example when we implementing the handle which already been taken by other users. We used variable name called handle_taken. As 'token' means silimar to handle, and it looks like 'taken'.When rest of our group member checking our code, they think we made a typing mistake. By avoiding that, we need more comments to explain our code.
## channel.py
channel_messages_v1:
    channel_messages_v1 relies on the data structure provided within data.py.
### helper_channel.py
Search Type:
    Search type is specified using integers corresponding to index in dictionary unless otherwise specified. The same legend (specified below) is used across both helper functions.

- 0 = channel_id
- 1 = channel_name
- 2 = is_public 
- 3 = is_owner
Search Term:
    The helper functions are currently built to handle channel_id as the input for search_term, however this may be updated in future iterations.
## channels.py
channels_create_v1()
	If a channel is created with a name that already belongs to another channel, the channel will be created regardless such that there will be two channels with the same name but different channel ids

## user.py

## message.py 
message_id format
(1 - message sent in channel, 2 - message sent in dm)(three digit comprised of channel_id.zfill(3))(total num messages at time of send)
pinned and unpinned msgs:
- when first sent/created a msg is by default unpinned

## other.py

## data.py
dms - 
    'creator' = the person who created the dm. This cannot be changed. Creator cannot be removed and new creators cannot be added. 
    'members' = all members of the dm, including the creator
    'message_id' = will be different format to message_id for channel messages

## admin.py
Admin_remove()
    Assuming that the "Removed User" value is used to replace the removed user's name_first 
**Dreams** owners:
    The first user to create an account is automatically made 'owner' of **Dreams**
    Permission IDs: 1 = OWNER, 2 = MEMBER
    Trying to remove a user who is not an owner will raise an input error

## standup.py
    In order to achieve the functionality of standup functions. I need to make the change of the channels data structure. Add is_active, time_finish and length to the structure. But the change of the exsiting data structure might lead to changing of large amount of code. Therefore. I decided to add a new data structure to the database. A new data base called standup will be created once the channel is created. And the keys and values mentioned above will be store inside this data struture.
