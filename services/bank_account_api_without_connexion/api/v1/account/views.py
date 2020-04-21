#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from api import (
    bcrypt,
    BankApiError,
    mongo
)
from api.models import (
    User,
    USER_ADMIN_ROLE
)

from api.utils.common import (
    api_authorization_check,
    isEmail,
    validInput
)

from flask import (
    g,
    Blueprint,
    jsonify,
    make_response,
    request
)
from flask.views import MethodView
import json

logger = logging.getLogger(__name__)
account_blueprint = Blueprint('account', __name__)
account_blueprint.before_request(api_authorization_check)

def isNotAdmin():
	current_user = g.current_user
	post_data = g.request_data

	if current_user['role'] != USER_ADMIN_ROLE:
		raise BankApiError(error_code='E9002', status_code=401)

class AccountAPI(MethodView):
	def get(self, account_number):
		accounts = mongo.db.accounts
		if account_number is None:
			# return a list of accounts
			accounts = mongo.db.accounts
			query_params = request.args
			output = []
			page_size = int(query_params.get('page_size'))
			page_index = int(query_params.get('page_index'))
			skips = page_size * page_index
			order_by = query_params.get('order_by')
			order_direction = int(query_params.get('order_direction'))
			where = json.loads(query_params.get('account'))
			data = accounts.find(where).sort(order_by, order_direction).skip(skips).limit(page_size)
			total = data.count()
			for account in data:
				output.append({
					'account_number': account['account_number'], 'balance': account['balance'], 'firstname' : account['firstname'], "lastname" : account['lastname'],
					'age' : account['age'], 'gender' : account['gender'], 'address' : account['address'], 'employer' : account['employer'],
					'email' : account['email'], 'city' : account['city'], 'state' : account['state']
				})
			return jsonify({
				'success': 1,
				'data': output,
				'total': total,
				'page_size': page_size,
				'page_index': page_index
			})
		else:
			# expose a single account
			account = accounts.find_one({'account_number' : int(account_number)})
			if account:
				output = {
				'account_number': account['account_number'], 'balance': account['balance'], 'firstname' : account['firstname'], "lastname" : account['lastname'],
				'age' : account['age'], 'gender' : account['gender'], 'address' : account['address'], 'employer' : account['employer'],
				'email' : account['email'], 'city' : account['city'], 'state' : account['state']
				}
				return jsonify({
					'success': 1,
					'data' : output
				})
			else:
				return jsonify({
					'success': 0,
					'message': 'No records found'
			})

	def post(self):
		accounts = mongo.db.accounts
		isNotAdmin()
		# accounts.create_index( [("account_number", PyMongo.TEXT), ("email", PyMongo.ASCENDING)],unique=True)
		post_data = request.get_json()

		#valid input
		validInput(post_data)
		account = accounts.find_one({'account_number' : int(post_data['account_number'])})
		if account:
			return jsonify({
				'success': 0,
				'message' : 'Duplicate account number'
			})

		account = accounts.find_one({'email' : post_data['email']})
		if account:
			return jsonify({
				'success': 0,
				'message' : 'Duplicate email'
			})

		account_id = accounts.insert(post_data)
		new_account = accounts.find_one({'_id' : account_id})
		output = {
			'account_number': new_account['account_number'], 'balance': new_account['balance'], 'firstname' : new_account['firstname'], "lastname" : new_account['lastname'],
			'age' : new_account['age'], 'gender' : new_account['gender'], 'address' : new_account['address'], 'employer' : new_account['employer'],
			'email' : new_account['email'], 'city' : new_account['city'], 'state' : new_account['state']
		}
		return jsonify({
			'success': 1,
			'data' : output,
            'message': 'Create successfully'
		})

	def put(self, account_number):
		accounts = mongo.db.accounts
		isNotAdmin()
		post_data = request.get_json()
		where = { "account_number": int(account_number) }

		#valid input
		validInput(post_data)
		email = accounts.find_one(where)['email']
		if email != post_data['email']:
			account = accounts.find_one({'email' : post_data['email']})
			if account:
				return jsonify({
					'success': 0,
					'message' : 'Duplicate email'
				})

		newvalues = { "$set": post_data }
		accounts.update_one(where, newvalues)
		return jsonify({
			'success': 1,
			'message': 'Update successfully'
		})

	def delete(self, account_number):
		accounts = mongo.db.accounts
		isNotAdmin()
		where = { "account_number": int(account_number) }
		accounts.delete_one(where)
		return jsonify({
			'success': 1,
			'message': 'Delete successfully'
		})

# define the API resources
account_view = AccountAPI.as_view('account_api')

# add Rules for API Endpoints
account_blueprint.add_url_rule(
	'',
	defaults={'account_number': None},
	view_func=account_view,
	methods=['GET']
)
account_blueprint.add_url_rule(
	'',
	view_func=account_view,
	methods=['POST']
)
account_blueprint.add_url_rule(
	'/<account_number>',
	view_func=account_view,
	methods=['GET', 'PUT', 'DELETE']
)
