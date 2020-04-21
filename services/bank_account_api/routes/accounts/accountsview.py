#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from app import (
    bcrypt,
    mongo,
    models
)

from utils.common import (
    validInput
)

from flask import (
    g,
    jsonify,
    request
)
from flask.views import MethodView
from werkzeug.exceptions import Unauthorized
import json

logger = logging.getLogger(__name__)

def isNotAdmin():
	current_user = g.current_user
	if current_user['role'] != models.USER_ADMIN_ROLE:
		raise Unauthorized('You are not allowed to use this action.')

class AccountsView(MethodView):
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

	def get(self, id):
		accounts = mongo.db.accounts
		# expose a single account
		account = accounts.find_one({'account_number' : int(id)})
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

	def put(self, id):
		accounts = mongo.db.accounts
		isNotAdmin()
		post_data = request.get_json()
		where = { "account_number": int(id) }

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

	def delete(self, id):
		accounts = mongo.db.accounts
		isNotAdmin()
		where = { "account_number": int(id) }
		accounts.delete_one(where)
		return jsonify({
			'success': 1,
			'message': 'Delete successfully'
		})

	def search(self):
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
