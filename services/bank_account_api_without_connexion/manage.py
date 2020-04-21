#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import json
from bson import json_util

from api import (
    app,
    mongo
)
from api.models import User

from flask_script import (
    Manager,
    Server
)

logger = logging.getLogger(__name__)
http_address = app.config.get('HTTP_ADDRESS')
http_port = app.config.get('HTTP_PORT')

manager = Manager(app)
manager.add_command('runserver', Server(host=http_address, port=http_port))

@manager.command
def seed_db():
    """
    Seed DB with accounts.json

    Decorators:
        manager.command
    """

    # TODO: Create user
    userNormal = User(username = 'usernormal', password = 'usernormal', role = 1)
    userAdmin = User(username = 'useradmin', password = 'useradmin', role = 10)
    User.insert(userNormal)
    User.insert(userAdmin)
    print('Seed User')

    # read accounts.json
    with open('./data/accounts.json') as f:
        accounts_data = json.load(f)
    mongo.db.accounts.insert_many(accounts_data)
    print('Seed Accounts')

if __name__ == '__main__':
    manager.run()
