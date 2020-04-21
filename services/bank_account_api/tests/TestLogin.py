import json

from api.models import BaseCase
from utils.common import (
    encode_access_token
)

class TestLogin(BaseCase):

    def test_successful_login(self):
        # Given
        username = "useradmin"
        password = "useradmin"
        payload = json.dumps({
            "username": username,
            "password": password
        })

        access_token = encode_access_token(username)
        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(access_token.decode(), response.json['access_token'])
        self.assertEqual(200, response.status_code)

    def test_login_with_incorrect_password(self):
        # Given
        username = "useradmin"
        password = "123456"
        payload = {
            "username": username,
            "password": password
        }

        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertEqual('Incorrect password.', response.json['message'])
        self.assertEqual(200, response.status_code)

    def test_login_with_user_not_exist(self):
        # Given
        username = "123456"
        password = "123456"
        payload = {
            "username": username,
            "password": password
        }

        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        # Then
        self.assertEqual("User isn't exist.", response.json['message'])
        self.assertEqual(200, response.status_code)
