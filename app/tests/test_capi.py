import base64
import json
import pytest
import requests
#
from Lost_And_Found.app.tests.test_base import BaseTestCase


class UserTest(BaseTestCase):
    url = 'http://127.0.0.1:5000'  # The root url of the flask app

    @pytest.fixture(scope='module')
    def token_re(self):
        usrPass = "mr.mucheema1@gmail.com:123456"
        data_bytes = usrPass.encode("utf-8")
        b64Val = base64.b64encode(data_bytes)

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic %s" % b64Val.decode("utf-8")
        }
        payload = ''

        response = requests.request("GET", self.url + '/user/login', data=payload, headers=headers)
        return response.json()

    def test_register_user(self):
        data = {"email": "muhammad.usama1@wanclouds.net", "password": "123456"}
        payload = json.dumps(data)
        headers = {
            'Content-Type': "application/json"

        }
        response = requests.request("POST", self.url + '/user/register', data=payload, headers=headers)
        assert response.status_code == 200

    def test_login_user(self):
        user_pass = "muhammad.usama@wanclouds.net:123456"
        data_bytes = user_pass.encode("utf-8")
        b64val = base64.b64encode(data_bytes)

        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic %s" % b64val.decode("utf-8")
        }
        payload = ''

        response = requests.request("GET", self.url + '/user/login', data=payload, headers=headers)
        assert response.status_code == 401

    def test_ge_all_post(self, token_re):
        headers = {'access-token': token_re['token']}
        response = requests.request("GET", self.url + '/post', headers=headers)
        assert response.status_code == 404

    def test_search_item(self, token_re):
        headers = {'access-token': token_re['token']}
        response = requests.request("GET", self.url + '/post/loptop', headers=headers)
        assert response.status_code == 404

        # def test_new_user(new_user):
        #     """
        #     GIVEN a User model
        #     WHEN a new User is created
        #     THEN check the email, hashed_password, authenticated, and role fields are defined correctly
        #     """
        #     assert new_user.email == 'jfs33635@eveav.com'
        #     assert new_user.hashed_password != '1234'
        #     assert not new_user.authenticated
