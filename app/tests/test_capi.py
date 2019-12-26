import base64
import json
import requests

import pytest
from mock import patch

from Lost_And_Found.app.models.models import users, items
from Lost_And_Found.app.tests.conftest import db


def test_register_user(app_client, new_user):

    data = {"email": "zib77707@eveav.com", "password": "123456"}
    payload = json.dumps(data)
    headers = {"Content-Type": "application/json"}
    response = app_client.post("/user/register", data=payload, headers=headers)
    print(response.json)
    assert response.status_code == 409


def test_login_user(app_client):
    user_pass = "zib77707@eveav.com:123456"
    data_bytes = user_pass.encode("utf-8")
    b64val = base64.b64encode(data_bytes)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic %s" % b64val.decode("utf-8"),
    }
    payload = ""
    response = app_client.get("/user/login", data=payload, headers=headers)
    print(response.json)
    assert response.status_code == 200


def test_ge_all_post(app_client, get_token):
    print(get_token["token"])
    headers = {"access-token": get_token["token"]}
    response = app_client.get("/post", headers=headers)
    assert response.status_code == 404


def test_search_item(app_client, get_token):
    print(get_token["token"])
    headers = {"access-token": get_token["token"]}
    response = app_client.get("/post/laptop", headers=headers)
    assert response.status_code == 404


def test_add_post(app_client,get_token):

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\n{\"name\": \"laptop\", \"description\": \"hp zbook\", \"category\":\"lost\", \"location\": \"comsats\", \"date\": \"30-12-19\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'access-token': get_token["token"],
        'Content-Type': "multipart/form-data; boundary=--------------------------099924278551725800536919",

    }

    # data = {"name": "laptop", "description": "hp zbook", "category":"lost", "location": "comsats", "date": "30-12-19"}
    # payload = json.dumps(data)
    # headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    #            "access-token": get_token["token"]
    #            }
    response = app_client.post("/post", data=payload, headers=headers)
    print(response.json)
    assert response.status_code == 201