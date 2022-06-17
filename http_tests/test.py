import requests
from src.other import clear_v1
from src.auth import *
url = "http://127.0.0.1:8080/"

clear_v1()

# register
r = requests.post(f"{url}/auth/register/v2", json={
    "email": "nut919anan@gmail.com",
    "password": "nut12bodin",
    "name_first": "nut",
    "name_last": "anan"
})
payload = r.json()
token = payload["token"] + "sdflkjhsadlkfhlsakdj"
print(token)
# logout
r = requests.post(f"{url}/auth/logout/v1", json={
    "token": token
})


print(r.json())
