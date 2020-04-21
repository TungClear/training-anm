import json

from tests.BaseCase import BaseCase

class TestInvalidRequestUrl(BaseCase):

    def test_invalid_token(self):
        response = self.app.post('/auth/login123', headers={"Content-Type": "application/json"})

        self.assertEqual("E0104", response.json['error_code'])
        self.assertEqual(400, response.status_code)
