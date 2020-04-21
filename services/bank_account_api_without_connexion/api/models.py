#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json

from api import (
    app,
    bcrypt,
    mongo
)
from flask import jsonify

BASE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'
DEFAULT_LIMIT = 10
DEFAULT_SORT_ORDER = 'asc'
USER_NORMAL_ROLE = 1
USER_ADMIN_ROLE = 10
BANK_ACCOUNT_SEARCHABLE_FIELDS = [
    'account_number',
    'balance'
]

class User:
    """
    User Model

    Variables:
        username {str} -- Username
        password {str} -- Hashed Password
        role {int} -- User Role: 1 - Normal, 10 - Admin
    """

    def __init__(self, username, password, role):
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.role = role

    @staticmethod
    def insert(user):
        mongo.db.users.insert({
            "username": user.username,
            "password": user.password,
            "role": user.role,
        })

    @staticmethod
    def find(username):
        user = mongo.db.users.find_one({
            "username": username
        })
        return user

class Account:
    """
    Account Model

    Variables:
        account_number {int} -- Account Number
        balance {int} -- Account Balance
        firstname {str} -- First Name
        lastname {str} -- Last Name
        age {int} -- Age
        gender {str} -- Gender
        address {str} -- Address
        employer {str} -- Employer
        email {str} -- Email
        city {str} -- City
        state {str} -- State
    """

    def __init__(
        self, account_number, balance, firstname, lastname,
        age, gender, address, employer, city, state
    ):
        self.account_number = account_number
        self.balance = balance
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.address = address
        self.employer = employer
        self.city = city
        self.state = state

