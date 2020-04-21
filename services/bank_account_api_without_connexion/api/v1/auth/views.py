#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from api import (
    bcrypt,
    mongo
)
from api.models import User
from api.utils.common import (
    encode_access_token
)
from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)
from flask.views import MethodView

logger = logging.getLogger(__name__)
auth_blueprint = Blueprint('auth', __name__)

class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        post_data = request.get_json()

        username = post_data.get('username')
        password = post_data.get('password')

        # TODO Validate username/password
        if username is None:
            # TODO
            response_object = {
                'success': 0,
                'message': 'Username is required'
            }
            return (jsonify(response_object))

        if password is None:
            # TODO
            response_object = {
                'success': 0,
                'message': 'Password is required'
            }
            return (jsonify(response_object))

        try:
            user = User.find(username)
            # import pdb
            # pdb.set_trace()
            if not user:
                response_object = {
                    'success': 0,
                    'message': "User isn't exist."
                }
                return (jsonify(response_object))

            if bcrypt.check_password_hash(user['password'], password):
                access_token = encode_access_token(str(user['username']))
                if access_token:
                    response_object = {
                        'success': 1,
                        'message': 'Login successfully.',
                        'access_token': access_token.decode(),
                        'role': user['role']
                    }
                    return (jsonify(response_object))
            else:
                response_object = {
                    'success': 0,
                    'message': 'Incorrect password.'
                }
                return (jsonify(response_object))

        except Exception as error:
            logger.exception(error)

        response_object = {
            'success': 0,
            'message': 'Login failed. Please try again.'
        }
        return (jsonify(response_object))

# Define the API resources
login_view = LoginAPI.as_view('login_api')

# Add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)
