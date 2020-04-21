import json

from tests.BaseCase import BaseCase

class TestUpdateAccount(BaseCase):

    def test_update_account_successfully(self):
        # Given
        username = "useradmin"
        password = "useradmin"
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

        account_number = response.json['data']['account_number']

        # Then
        account_update_payload = {
            "balance": 500,
            "firstname": "tung123",
            "lastname": "nguyen123",
            "age": 36,
            "gender": "M",
            "address": "671 Bristol Street",
            "employer": "TungNX",
            "email": "tungnx@rk.com",
            "city": "Dante",
            "state": "TN"
        }
        response = self.app.put(f'/accounts/{account_number}',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            data=json.dumps(account_update_payload)
        )

        self.assertEqual(1, response.json['success'])
        self.assertEqual(200, response.status_code)
