import unittest

from api import (
    app,
    mongo
)
from api.models import User

class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # create database
        mongo.db.create_collection('users')
        mongo.db.create_collection('accounts')
        userNormal = User(username = 'usernormal', password = 'usernormal', role = 1)
        userAdmin = User(username = 'useradmin', password = 'useradmin', role = 10)
        User.insert(userNormal)
        User.insert(userAdmin)

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collectionName in mongo.db.collection_names():
            mongo.db.drop_collection(collectionName)
