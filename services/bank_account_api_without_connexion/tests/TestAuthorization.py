import json

from tests.BaseCase import BaseCase

class TestAuthorization(BaseCase):

    def test_authorization(self):
        # Given
        username = "usernormal"
        password = "usernormal"
        user_payload = json.dumps({
            "username": username,
            "password": password
        })

        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
        access_token = response.json['access_token']

        account_payload = {
            "account_number": 1002,
            "balance": 500,
            "firstname": "tung",
            "lastname": "nguyen",
            "age": 36,
            "gender": "M",
            "address": "671 Bristol Street",
            "employer": "TungNX",
            "email": "tungnx@rk.com",
            "city": "Dante",
            "state": "TN"
        }

        # When
        response = self.app.post('/accounts',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            data=json.dumps(account_payload)
        )

        # Then
        self.assertEqual("E9002", response.json['error_code'])
        self.assertEqual(401, response.status_code)
