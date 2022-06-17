"""
auth.py
    - include of 2 function
        - auth_register
        - auth_login
    - this auth module is about create an id and login to then idb
    - auth_register
        - parameter
            email password name_first name_last
        - return
            { auth_user_id }
        - description
            create id and save user information to data
        - side effect
            create changes in data
        - exceptions
            InputError return when the email password or names are not in the
            correct format, or the email is used by other users
    - auth_login
        - parameter
            email and password
        - return
            { auth_user_id }
        - description
            receive the email and password registered and return auth_user_id
        - side effect
            -
        - exception
            raise InputError when receive email and password not match,
            or email is not in correct format

"""
import re
from src.error import InputError
from src.utils import load_data, save_data, secret
import jwt
from jwt import InvalidSignatureError
import random


def auth_login_v2(email, password):
    """
    :param email:
    :param password:
    :return: token that have encoded session_id

    1. check email pattern
    2. find user with match email and password
    3. generate session_id for user
    4. encode session_id and return token
    """

    # check email pattern
    email_pattern = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.match(email_pattern, email):
        raise InputError("Invalid email")

    data = load_data()
    # find the user with the match email and password else return error
    u_id = search_user_id(email, password)
    if u_id is None:
        raise InputError()

    # generate session_id
    session_id = generate_session_id()

    # add the session_id to the session_ids
    # session_id in the session_ids is logged_in
    data["users"][u_id]["session_ids"].append(session_id)

    save_data(data)

    # encode the session_id and return it in token
    token = jwt.encode({"session_id": session_id}, secret, algorithm='HS256')
    return {
        "token": token,
        "auth_user_id": int(u_id)
    }


def auth_register_v2(email, password, name_first, name_last):
    """
    :param email: string with email format
    :param password: password with more than 6 character
    :param name_first: string between 1-50
    :param name_last: string between 1-50
    :return: token that have encoded session_id

    1. check name email password
    2. check if email used by other users
    3. generate session_id
    4. generate auth_user_id or u_id
    5. create user data and store in data
    6. encode session_id and return it in token

    """

    if (1 <= len(name_first) <= 50) and (1 <= len(name_last) <= 50):
        pass  # correct name format
    else:
        raise InputError

    email_format = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.match(email_format, email): # if not match return error
        raise InputError

    if len(password) < 6:
        raise InputError

    data = load_data()

    for user in data["users"]:
        if data["users"][user]["email"] == email:
            raise InputError

    session_id = generate_session_id()

    auth_user_id = 1000
    while str(auth_user_id) in data["users"]:
        auth_user_id += 1

    if auth_user_id == 1000:
        permission_id = 1
    else:
        permission_id = 2

    handle_str = generate_handle(name_first, name_last)
    session_id = generate_session_id()

    user = {
        "u_id": auth_user_id,
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
        "session_ids": [session_id],
        "handle_str": handle_str,
        "permission_id": permission_id
    }

    data["users"][auth_user_id] = user
    save_data(data)

    # encode to jwt format
    token = jwt.encode({"session_id": session_id}, secret, algorithm='HS256')
    return {
        "token": token,
        "auth_user_id": int(auth_user_id)
    }


def auth_logout_v1(token):
    """

    :param token: { "token": encoded(session_id) }
    :return: { is_success }
    1. decode the token for session_id
    2. find the owner of the sessio_id
    3. remove the session_id
    4. return the status of logout whether success or not
    """

    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except InvalidSignatureError:
        return{"is_success": False}
    session_id = payload["session_id"]

    data = load_data()
    is_success = False
    for u_id in data["users"]:
        if session_id in data["users"][u_id]["session_ids"]:
            is_success = True
            data["users"][u_id]["session_ids"].remove(session_id)
            is_success = True
    save_data(data)

    return {
        "is_success": is_success
    }


def generate_handle(name_first, name_last):
    """
    :param name_first:
    :param name_last:
    :return:
    generate session id based on the name_first and name_last also decorate the
    id if the id already taken
    1. format and concatenate name_first and name_last
    2. check existence of the
    3. if exist append number until it is unique
    """
    data = load_data()

    # concatenate the name_first and name_last
    handle = name_first + name_last
    handle = re.sub("[^a-zA-Z0-9]+", "", handle)  # remove special character
    handle = handle.lower()
    handle = handle[0:20]


    # list all the session_id
    users = data["users"]
    existed_handle = []
    for u_id in users:
        existed_handle.append(users[u_id]["handle_str"])

    # append the number if the handle taken

    i = 0
    edited_handle = handle
    while edited_handle in existed_handle:
        edited_handle = handle + str(i)
        i += 1

    return edited_handle


def auth_passwordreset_request_v1(email):
    """

    :param email: email for the user
    :return: reset_code: reset_code for the user
    1. create reset_code
    2. store it in the users data and send it to the email
    3. how to send the data from the funciton to flask
    4. this function could  return the reset code and in the flask
        it does not return
    """
    data = load_data()
    u_id = str(email_to_id(email))
    if u_id == "0":
        # not u_id found from this user
        reset_code = "invalid_email"
    else:
        reset_code = generate_reset_code()
        data["users"][u_id]["reset_code"] = reset_code

    save_data(data)
    return {
        "reset_code": reset_code,
    }



def auth_passwordreset_reset_v1(reset_code, new_password):
    """

    :param reset_code:
    :param new_password:
    :return:

    1. check the reset code is valid
    2. check the owner of the reset code
    3. check if password is valid or not
    """
    u_id = reset_code_to_uid(reset_code)
    if not u_id:
        raise InputError
    if len(new_password) < 6:
        raise InputError

    data = load_data()
    data["users"][str(u_id)]["password"] = new_password
    data["users"][str(u_id)].pop("reset_code")
    save_data(data)
    return {

    }


def generate_session_id():
    data = load_data()
    users = data["users"]

    existed_session_id = []

    for u_id in users:
        session_ids = users[u_id]["session_ids"]
        for session_id in session_ids:
            existed_session_id.append(session_id)

    new_session_id = 2000
    while new_session_id in existed_session_id:
        new_session_id += 1

    return new_session_id


def search_user_id(email, password):
    """
    find the user with match email and password
    :param email:
    :param password:
    :return: user_id
    """
    data = load_data()

    for u_id in data["users"]:
        user = data["users"][u_id]
        if user["email"] == email and user["password"] == password:
            return u_id


def generate_reset_code():
    """
    return: reset_code
    Generate reset code that is not existed
    by using choosing the uppercase letter randomly
    """
    data = load_data()
    users = data["users"]
    existed_reset_code = []
    for u_id in users:
        if "reset_code" in users[u_id]:
            reset_code = users[u_id]["reset_code"]
            existed_reset_code.append(reset_code)

    # assume that there is not a 10**10 reset request at a time
    reset_code = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVXYZ") for i in range(10))
    while reset_code in existed_reset_code:
        reset_code = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVXYZ") for i in range(10))

    return reset_code


def email_to_id(email):
    """

    :param email: user_email
    :return: u_id int
        return u_id of the owner email
        return 0 if the user is not exist or the email is not belong to any user
    """
    data = load_data()
    users = data["users"]
    for u_id in users:
        if users[u_id]["email"] == email:
            return int(u_id)
    return 0


def reset_code_to_uid(reset_code):
    """
    find the user that have the reset code and return the u_id(int)
    :param reset_code: reset_code(str)
    :return: u_id(int)
    """
    if not reset_code:
        return None

    data = load_data()
    users = data["users"]
    for u_id in users:
        if "reset_code" in users[u_id]:
            if reset_code == users[u_id]["reset_code"]:
                return int(u_id)
    return None


if __name__ == "__main__":
    from src.other import clear_v1
    clear_v1()
    handle1 = generate_handle("Camila","Moro")
    print(handle1)
    # not generate the same value in channels_http_test
    auth_register_v2("nut999anan@gmail.com", "nut12bodin", "Camila","Moro")
    auth_register_v2("nut555anan@gmail.com", "nut12bodin", "Camila","Moro")

