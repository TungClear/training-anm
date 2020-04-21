#!/usr/bin/env python

import os
from pathlib import Path
from dotenv import load_dotenv

import connexion
from connexion.resolver import MethodViewResolver

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask import (
    jsonify,
    make_response
)

from api import (
    models,
)
from flask_script import (
  Manager
)
import json

connex_app = connexion.FlaskApp(__name__)

# Get the underlying Flask app instance
app = connex_app.app

if os.getenv('APP_DOCKERIZED') != '1':
    env_path = Path(os.getcwd()) / '.env'
    load_dotenv(dotenv_path=env_path)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig',
)

app.config.from_object(app_settings)

CORS(app)
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
manager = Manager(app)

connex_app.add_api('swagger.yaml',
            arguments={'title': 'Bank Account Backend Swagger'},
            resolver=MethodViewResolver('routes'))

@manager.command
def seed_db():
    """
    Seed DB with accounts.json

    Decorators:
        manager.command
    """

    # TODO: Create user
    userNormal = models.User(username = 'usernormal', password = 'usernormal', role = 1)
    userAdmin = models.User(username = 'useradmin', password = 'useradmin', role = 10)
    models.User.insert(userNormal)
    models.User.insert(userAdmin)
    print('Seed User')

    # read accounts.json
    with open('./data/accounts.json') as f:
        accounts_data = json.load(f)
    mongo.db.accounts.insert_many(accounts_data)
    print('Seed Accounts')

@manager.command
def runserver():
  connex_app.run(port=8080)

if __name__ == '__main__':
    manager.run()
