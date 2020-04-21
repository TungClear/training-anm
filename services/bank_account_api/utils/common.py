#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import (
    datetime,
    timedelta
)
import logging
from logging import handlers
import re

from app import (
    models,
    app
)

from flask import (
    g,
    request,
    jsonify
)
import jwt
import re
from werkzeug.exceptions import Unauthorized, BadRequest

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


def api_authorization_check(access_token):
    """
    Check valid request

    Returns:
        flask.Response
    """
    user = None
    
    if access_token:
        try:
            decoded_access_token = decode_access_token(access_token)
            username = decoded_access_token['sub']
            user = models.User.find(username=username)
            if not user:
                raise Unauthorized('Invalid token.')
        except:
                raise Unauthorized('Invalid token.')
    else:
        raise Unauthorized('Invalid token.')

    g.current_user = user
    return user

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
        raise BadRequest('Age must be number')
    elif (input['age'] <= 0):
        raise BadRequest('Age must be greater than 0')
    if not isInteger(input['balance']):
        raise BadRequest('Balance must be number')
    elif (input['balance'] < 0):
        raise BadRequest('Balance must be greater or equal than 0')
    if not isEmail(input['email']):
        raise BadRequest('Email must be valid')
