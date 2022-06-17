"""Importing functions"""
from src.dm import dm_list_v1
from src.channels import channels_list_v2
from src.utils import load_data, save_data, token_to_id
from src.error import InputError


def clear_v1():
    """
    clear all data in data.json
    :return:
    """
    data = load_data()

    data = {
    "users": {},
    "channels": {},
    "channel_info": {},
    "channel_standup": {},
    "messages": {
        "total": 0,
    },
    "notifications": {},
    "dms": {},
    "dm_messages": {}
}
    # for key in data:
        # data[key].clear()
    save_data(data)


def search_v1(token, query_str):
    """
    :param token:
    :param query_str:
    :return:
    Returns list of messages that match query_str
    """
    data = load_data()
    search_result = []

    if len(query_str) > 1000:
        raise InputError

    result = channels_list_v2(token)
    channels_details = result["channels"]
    channel_ids = []
    for detail in channels_details:
        channel_ids.append(detail["channel_id"])

    result = dm_list_v1(token)
    dms_details = result["dms"]
    dm_ids = []
    for detail in dms_details:
        dm_ids.append(detail["dm_id"])

    dm_messages = [data["dm_messages"][f"{dm_id}"]["messages"] for dm_id in dm_ids]
    for messages in dm_messages:
        for message_detail in messages:
            if query_str in message_detail["message"]:
                search_result.append(message_detail)

    channel_message = [data["messages"][f"{channel_id}"]["messages"] for channel_id in channel_ids]
    for messages in channel_message:
        for message_detail in messages:
            if query_str in message_detail["message"]:
                search_result.append(message_detail)

    return {
        "messages": search_result
    }


if __name__ == "__main__":
    clear_v1()
