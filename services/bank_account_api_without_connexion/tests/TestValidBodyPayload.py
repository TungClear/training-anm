import json

from tests.BaseCase import BaseCase

class TestValidBodyPayload(BaseCase):

    def test_age_must_number(self):
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
            "age": '36',
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
        self.assertEqual('E1001', response.json['error_code'])
        self.assertEqual(400, response.status_code)

    def test_balance_must_number(self):
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
            "balance": '500',
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
        self.assertEqual('E1003', response.json['error_code'])
        self.assertEqual(400, response.status_code)

    def test_age_must_greater_1(self):
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
            "age": 0,
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
        self.assertEqual('E1002', response.json['error_code'])
        self.assertEqual(400, response.status_code)

    def test_balance_must_positive(self):
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
            "balance": -1,
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
        self.assertEqual('E1004', response.json['error_code'])
        self.assertEqual(400, response.status_code)

    def test_email_not_valid(self):
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
            "email": "tungnx.com",
            "city": "Dante",
            "state": "TN"
        }

        # When
        response = self.app.post('/accounts',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            data=json.dumps(account_payload)
        )

        # Then
        self.assertEqual('E1005', response.json['error_code'])
        self.assertEqual(400, response.status_code)

    def test_duplicate_account_number(self):
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
        response = self.app.post('/accounts',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            data=json.dumps(account_payload))

        # When
        response = self.app.post('/accounts',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            data=json.dumps(account_payload))

        # Then
        self.assertEqual(0, response.json['success'])
        self.assertEqual('Duplicate account number', response.json['message'])
        self.assertEqual(200, response.status_code)

    def test_duplicate_email(self):
        # Given
        username = "useradmin"
        password = "useradmin"
        user_payload = json.dumps({
            "username": username,
            "password": password
        })

        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
        access_token = response.json['access_token']

        account1_payload = {
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
        response = self.app.post('/accounts',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            data=json.dumps(account1_payload))

        account2_payload = {
            "account_number": 1003,
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
            data=json.dumps(account2_payload))

        # Then
        self.assertEqual(0, response.json['success'])
        self.assertEqual('Duplicate email', response.json['message'])
        self.assertEqual(200, response.status_code)
