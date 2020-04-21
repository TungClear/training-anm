import json

from api.models import BaseCase

class TestInvalidRequestUrl(BaseCase):

    def test_invalid_token(self):
        response = self.app.post('/login123', headers={"Content-Type": "application/json"})

        self.assertEqual("Not Found", response.json['title'])
        self.assertEqual(404, response.status_code)
