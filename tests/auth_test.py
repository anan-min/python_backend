from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.auth import auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import InputError
from src.other import clear_v1
import pytest


# test for auth_register_v2
def test_register_invalid_email():
    """test for invalid email format"""
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("notemail", "password", "firstname", "lastname")


def test_register_registered_email():
    """# test for registered email"""
    clear_v1()
    auth_register_v2("test@email.com", "password", "firstname", "lastname")
    with pytest.raises(InputError):
        auth_register_v2("test@email.com", "password", "firstname", "lastname")


def test_register_inadequate_password_length():
    """test for password shorter than 6 character"""
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("test@email.com", "123", "firstname", "lastname")


def test_register_prolonged_name_first():
    """test for name_first that exceed the range(0-50)"""
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("test@email.com", "password", "c"*51, "lastname")


def test_register_prolonged_name_last():
    """test for name_last that exceed the range(0-50)"""
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2("test@email.com", "password", "firstname", "c"*51)


# test for auth_login_v2()
def test_login_incorrect_login_email_format():
    """incorrect email format"""
    clear_v1()
    auth_register_v2("test@email.com", "password", "name2", "name2")
    with pytest.raises(InputError):
        auth_login_v2("not_email", "password")


def test_login_email_not_registered():
    """email is not registered"""
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v2("notregistered@email.com", "password")


def test_login_password_incorrect():
    """password incorrect"""
    clear_v1()
    auth_register_v2("test@email.com", "password", "name3", "name3")
    with pytest.raises(InputError):
        auth_login_v2("test@email.com", "incorrectpassword")



"""
test for auth_logout_v1
1. all Error cases InputError and AccessError(N/A)
2. check the usage of the logout
    2.1 successful
        2.1.1 register logout
        2.1.2 register login logout logout
    2.2 failed
        2.2.1 invalid token 
        2.2.2 register logout logout   
"""


def test_logout_successful1():
    clear_v1()
    # register
    r = auth_register_v2("nut999anan@gmail.com", "nut12bodin", "nut", "anan")
    token = r["token"]
    # logout
    r = auth_logout_v1(token)
    is_success = r["is_success"]

    assert is_success


def test_logout_successful2():
    clear_v1()
    # register
    r = auth_register_v2("nut999anan@gmail.com", "nut12bodin", "nut", "anan")
    token1 = r["token"]
    # login
    r = auth_login_v2("nut999anan@gmail.com", "nut12bodin")
    token2 = r["token"]
    # logout
    r = auth_logout_v1(token1)
    is_success1 = r["is_success"]
    # logout
    r = auth_logout_v1(token2)
    is_success2 = r["is_success"]

    assert is_success1
    assert is_success2


def test_logout_failed1():
    clear_v1()

    # register
    r = auth_register_v2("nut999anan@gmail.com", "nut12bodin", "nut", "anan")
    token1 = r["token"]

    # login
    r = auth_login_v2("nut999anan@gmail.com", "nut12bodin")
    token2 = r["token"]

    # logout
    r = auth_logout_v1(token1)
    is_success1 = r["is_success"]

    # logout
    r = auth_logout_v1(token2)
    # logout
    r = auth_logout_v1(token2)

    is_success2 = r["is_success"]

    assert is_success1
    assert not is_success2


def test_logout_failed2():
    clear_v1()
    # register
    r = auth_register_v2("nut999anan@gmail.com", "nut12bodin", "nut", "anan")
    token = r["token"]
    # logout
    r = auth_logout_v1(token)
    r = auth_logout_v1(token)
    is_success = r["is_success"]
    assert not is_success

# auth_passwordreset_request_v1(), auth_passwordreset_reset_v1()


def test_passwordreset_reset_error1():
    clear_v1()
    # what is a correct reset code
    # the password is less than  6 character
    password = "password"
    email = "test1@mail.com"
    auth_register_v2(email, password, "nut", "anan")
    reset_request_result = auth_passwordreset_request_v1(email)
    reset_code = reset_request_result["reset_code"]
    new_password = "1"

    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(reset_code, new_password)


def test_passwordreset_reset_error2():
    clear_v1()
    # what is a correct reset code
    # the password is less than  6 character
    password = "password"
    email = "test1@mail.com"
    auth_register_v2(email, password, "nut", "anan")
    auth_passwordreset_request_v1(email)

    new_password = "new_password"

    with pytest.raises(InputError):
        auth_passwordreset_reset_v1("not correct reset code", new_password)


def test_reset_password():
    clear_v1()
    # what is a correct reset code
    # the password is less than  6 character
    password = "password"
    email = "nut999anan@hotmail.com"
    register_result = auth_register_v2(email, password, "nut", "anan")
    reset_request_result = auth_passwordreset_request_v1(email)
    reset_code = reset_request_result["reset_code"]

    new_password = "new_password"
    auth_passwordreset_reset_v1(reset_code, new_password)

    login_result = auth_login_v2(email, new_password)
    assert register_result["auth_user_id"] == login_result["auth_user_id"]

