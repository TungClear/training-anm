#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class BaseConfig:
    """
    Base configuration.
    """
    PRODUCTION = False
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    APP_DOMAIN = os.getenv('APP_DOMAIN')
    HTTP_PORT = os.getenv('HTTP_PORT')
    HTTP_ADDRESS = os.getenv('HTTP_ADDRESS')
    JWT_SECRET = os.getenv('JWT_SECRET', 'default_secret')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI')

class DevelopmentConfig(BaseConfig):
    """
    Development configuration.

    Extends:
        BaseConfig
    """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4

class TestingConfig(BaseConfig):
    """
    Testing configuration.

    Extends:
        BaseConfig
    """
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_DBNAME = os.getenv('MONGO_DBNAME') + '_test'
    MONGO_URI = os.getenv('MONGO_URI') + '_test'


class ProductionConfig(BaseConfig):
    """
    Production configuration.

    Extends:
        BaseConfig
    """
    PRODUCTION = True
    DEBUG = False
