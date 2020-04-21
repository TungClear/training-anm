import json

from api.models import BaseCase

class TestGetAccount(BaseCase):

    def test_get_account_successfully(self):
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
            data=json.dumps(account_payload))

        account_number = response.json['data']['account_number']

        # Then
        response = self.app.get(f'/accounts/{account_number}',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})
        created_account = response.json['data']

        self.assertEqual(account_payload['balance'], created_account['balance'])
        self.assertEqual(account_payload['firstname'], created_account['firstname'])
        self.assertEqual(account_payload['age'], created_account['age'])
        self.assertEqual(account_payload['gender'], created_account['gender'])
        self.assertEqual(account_payload['address'], created_account['address'])
        self.assertEqual(account_payload['employer'], created_account['employer'])
        self.assertEqual(account_payload['email'], created_account['email'])
        self.assertEqual(account_payload['city'], created_account['city'])
        self.assertEqual(account_payload['state'], created_account['state'])
        self.assertEqual(1, response.json['success'])
        self.assertEqual(200, response.status_code)

    def test_get_account_fail(self):
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
            data=json.dumps(account_payload))

        account_number = response.json['data']['account_number']

        # Then
        response = self.app.get(f'/accounts/{account_number+1}',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})

        self.assertEqual('No records found', response.json['message'])
        self.assertEqual(0, response.json['success'])
        self.assertEqual(200, response.status_code)
