#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import (
    datetime,
    timedelta
)
import decimal
import logging
from logging import handlers
import math
import os
import sys
import subprocess
import re

from api import (
    BankApiError,
    app
)
from api.models import (
    User,
    Account
)

from flask import (
    g,
    request,
    jsonify
)
import jwt
import re

logger = logging.getLogger(__name__)

def encode_access_token(user_name):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_name
        }
        return jwt.encode(
            payload,
            app.config.get('JWT_SECRET'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_access_token(access_token):
    """
    Validates the auth token
    :param access_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(access_token, app.config.get('JWT_SECRET'))
        return payload
    except jwt.ExpiredSignatureError:
        return 'Your token is expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def api_authorization_check():
    """
    Check valid request

    Returns:
        flask.Response
    """
    request_data = None
    user = None

    if request.method != 'OPTIONS':
        # Decode JWT Token <access_token>
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                access_token = auth_header.split(' ')[1]
            except IndexError:
                raise BankApiError(error_code='E9001', status_code=401)
        else:
            raise BankApiError(error_code='E9001', status_code=401)

        if access_token:
            try:
                decoded_access_token = decode_access_token(access_token)
                username = decoded_access_token['sub']
                user = User.find(username=username)
                if not user:
                    raise BankApiError(error_code='E9001', status_code=401)
            except:
                 raise BankApiError(error_code='E9001', status_code=401)

        logger.info(request_data)

        g.request_data = request_data
        g.current_user = user

# Make a regular expression
# for validating an Email
regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'

# Define a function for
# for validating an Email
def isEmail(email):
    # pass the regualar expression
    # and the string in search() method
    return re.search(regex,email)

def isInteger(value):
    return type(value) is int

def validInput(input):
    if not isInteger(input['age']):
        raise BankApiError(error_code='E1001', status_code=400)
    elif (input['age'] <= 0):
        raise BankApiError(error_code='E1002', status_code=400)
    if not isInteger(input['balance']):
        raise BankApiError(error_code='E1003', status_code=400)
    elif (input['balance'] < 0):
        raise BankApiError(error_code='E1004', status_code=400)
    if not isEmail(input['email']):
        raise BankApiError(error_code='E1005', status_code=400)
