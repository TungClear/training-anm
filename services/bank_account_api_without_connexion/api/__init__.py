#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging import handlers
import os
from pathlib import Path

from .messages import ERROR_MESSAGES

from dotenv import load_dotenv
from flask import (
    current_app,
    Flask,
    jsonify,
    make_response
)
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')
CORS(app)

if os.getenv('APP_DOCKERIZED') != '1':
    env_path = Path(os.getcwd()) / '.env'
    load_dotenv(dotenv_path=env_path)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig',
)
app.config.from_object(app_settings)

babel = Babel(app)

# Set logging level
if app.config.get('DEBUG') is True:
    log_level = logging.DEBUG
else:
    log_level = logging.ERROR

LOG_FILENAME = 'logs/bank-account-api.log'
handler = handlers.TimedRotatingFileHandler(
    LOG_FILENAME, when='midnight')
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(log_level)
logging.basicConfig(
    filename=LOG_FILENAME,
    level=log_level,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

bcrypt = Bcrypt(app)
mongo = PyMongo(app)

class BankApiError(Exception):
    """
    Bank API Exception
    """
    status_code = 200
    error_code = 'E0000'

    def __init__(
        self,
        message=None,
        error_code=None,
        status_code=None,
        params=None
    ):
        Exception.__init__(self)
        self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

        if error_code == 'E0000':
            self.status_code = 400

        if not message:
            message = ERROR_MESSAGES[error_code]

        if params:
            if type(params) == tuple or type(params) == list:
                self.message = message.format(*params)
            elif type(params) == dict:
                self.message = message.format(**params)
            elif type(params) == str or type(params) == int:
                self.message = message.format(params)
            else:
                self.message = message
        else:
            self.message = message
        logger_server = logging.getLogger()
        logger_server.info(message)

    def to_dict(self):
        """
        To dict
        """
        return {
            'result': False,
            'error': self.message,
            'error_code': self.error_code
        }

@app.errorhandler(404)
def page_not_found(_):
    error_code = 'E0104'
    error_message = ERROR_MESSAGES[error_code]
    response_object = {
        'result': False,
        'error': error_message,
        'error_code': error_code
    }
    return make_response(jsonify(response_object)), 400


@app.errorhandler(405)
def method_not_allowed(_):
    error_code = 'E0103'
    error_message = ERROR_MESSAGES[error_code]
    response_object = {
        'result': False,
        'error': error_message,
        'error_code': error_code
    }
    return make_response(jsonify(response_object)), 400


@app.errorhandler(500)
def internal_server_error(_):
    error_code = 'E0105'
    error_message = ERROR_MESSAGES[error_code]
    response_object = {
        'result': False,
        'error': error_message,
        'error_code': error_code
    }
    return make_response(jsonify(response_object)), 500


@app.errorhandler(BankApiError)
def handle_bank_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


from .v1.auth.views import auth_blueprint
from .v1.account.views import account_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(account_blueprint, url_prefix='/accounts')
