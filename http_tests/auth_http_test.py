import pytest
import requests
from src.other import clear_v1


url = "http://127.0.0.1:8080/"


def test_logout_successful1():
    clear_v1()

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut919anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "Nut",
        "name_last": "Anan"
    })

    payload = r.json()
    token = payload["token"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token
    })

    payload = r.json()
    is_success = payload["is_success"]

    assert is_success


def test_logout_successful2():
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut1anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "nut",
        "name_last": "anan"
    })
    payload = r.json()
    token1 = payload["token"]

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut2anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "nut",
        "name_last": "anan"
    })
    payload = r.json()
    token2 = payload["token"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token1
    })
    payload = r.json()
    is_success1 = payload["is_success"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token2
    })
    payload = r.json()
    is_success2 = payload["is_success"]

    assert is_success1
    assert is_success2


def test_logout_failed1():
    clear_v1()
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut1anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "nut",
        "name_last": "anan"
    })
    payload = r.json()
    token = payload["token"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token
    })
    payload = r.json()
    is_success1 = payload["is_success"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token
    })
    payload = r.json()
    is_success2 = payload["is_success"]

    assert is_success1
    assert not is_success2


def test_logout_failed2():
    clear_v1()
    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut1anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "nut",
        "name_last": "anan"
    })
    payload = r.json()
    token1 = payload["token"]

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut2anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "nut",
        "name_last": "anan"
    })
    payload = r.json()
    token2 = payload["token"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token1
    })
    payload = r.json()
    is_success1 = payload["is_success"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token2
    })
    payload = r.json()
    is_success2 = payload["is_success"]

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token2
    })
    payload = r.json()
    is_success3 = payload["is_success"]

    assert is_success1
    assert is_success2
    assert not is_success3


def test_logout_failed3():
    clear_v1()

    # register
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut919anan@gmail.com",
        "password": "nut12bodin",
        "name_first": "Nut",
        "name_last": "Anan"
    })
    payload = r.json()
    # invalid token
    token = payload["token"] + "asdlkjh"

    # logout
    r = requests.post(f"{url}/auth/logout/v1", json={
        "token": token
    })
    payload = r.json()
    is_success = payload["is_success"]

    assert not is_success


def test_passwordreset_request():
    clear_v1()
    """
    check status code of normal request
    check status code of email that is not belong to user
    """
    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut999anan@hotmail.com",
        "password": "nut12bodin",
        "name_first": "Nut",
        "name_last": "Anan"
    })
    assert r.status_code == 200

    r = requests.post(f"{url}/auth/passwordreset/request/v1", json={
        "email": "nut999anan@hotmail.com"
    })
    assert r.status_code == 200

    # not registered email
    r = requests.post(f"{url}/auth/passwordreset/request/v1", json={
        "email": "test1@gmail.com"
    })

    assert r.status_code == 200


def test_passwordreset_reset():
    clear_v1()

    r = requests.post(f"{url}/auth/register/v2", json={
        "email": "nut999anan@hotmail.com",
        "password": "nut12bodin",
        "name_first": "Nut",
        "name_last": "Anan"
    })
    assert r.status_code == 200

    r = requests.post(f"{url}/auth/passwordreset/request/v1", json={
        "email": "nut999anan@hotmail.com"
    })
    assert r.status_code == 200

    # status code invalid
    r = requests.post(f"{url}/auth/passwordreset/reset/v1", json={
        "reset_code": "",
        "new_password": "password",
    })
    assert r.status_code == 500

    # password length invalid and status code invalid
    r = requests.post(f"{url}/auth/passwordreset/reset/v1", json={
        "reset_code": "",
        "new_password": "1",
    })
    assert r.status_code == 500

