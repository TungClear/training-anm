import json

from api.models import BaseCase

class TestDeleteAccount(BaseCase):

    def test_update_account_successfully(self):
        # Given
        username = "useradmin"
        password = "useradmin"
        user_payload = json.dumps({
            "username": username,
            "password": password
        })

        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=user_payload)
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
        response = self.app.delete(f'/accounts/{account_number}',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        )

        self.assertEqual(1, response.json['success'])
        self.assertEqual(200, response.status_code)
