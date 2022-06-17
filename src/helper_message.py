""" Helper functions for message.py """

from src.error import AccessError, InputError
from src.utils import load_data, save_data

def message_author(u_id, message_id, m_list):
    for m in m_list:
        if m["message_id"] == message_id:
            if m["u_id"] == "Removed user":
                return "Removed user"
            return int(m["u_id"]) == int(u_id)

def find_message_text(message_id):
    
    data = load_data()

    message_id = message_id["message_id"]

    # Message id belongs to channel
    if str(message_id)[0] == '1':
        m_list = data["messages"][str(int(str(message_id)[1:4]))]["messages"]
        for m in m_list:
            if m["message_id"] == message_id:
                return m["message"]
    else:
        m_list = data["dm_messages"][str(int(str(message_id)[1:5]))]["messages"]
        for m in m_list:
            if m["message_id"] == message_id:
                return m["message"]


def delete_user_messages(u_id):

    data = load_data()
    if not len(data["messages"]) > 1:
        pass
    else:
        for channel in data["messages"]:
            for message in data["messages"][channel]:
                if message["u_id"] == u_id:
                    data["messages"][channel]["messages"]["message"] = "Removed user"

    for dm_id in data["dm_messages"]:
        for message in data["dm_messages"][dm_id]["messages"]:
            if message["u_id"] == u_id:
                message["message"] = "Removed user"
    save_data(data)
