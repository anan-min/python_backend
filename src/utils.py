import json
import random
import jwt
from os import chdir, getcwd 

# secret for jwt encode
secret = "THIS_IS_SECRET"


def load_data(file_name="data.json"):
    """
    load data from file with path and return it
    :param file_name:
    :return:
    """
    if getcwd().endswith('project-backend'):
        chdir('src')
    else:
        chdir('../src')
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
        json_file.close()
        return data


def save_data(data, file_name = "data.json"):
    """
    save data to file with path
    :param data:
    :param file_name:
    :return:
    """

    if getcwd().endswith('project-backend'):
        chdir('src')
    else:
        chdir('../src')
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
        json_file.close()


def token_to_id(token):
    """
    given the token(encode session_id) return the owner u_id
    :param token:
    :return: u_id of the token owner

    1. decode the token to session_id
    2. loop through each user
    ( each user data store in users[u_id] )
    3. check if the session_id in user["session_ids"]
    """
    # decode the token from jwt
    payload = jwt.decode(token, secret, algorithms='HS256')
    session_id = payload["session_id"]
    # find the owner of session_id
    data = load_data()
    for u_id in data["users"]:
        user = data["users"][u_id]
        if session_id in user["session_ids"]:
            return u_id

