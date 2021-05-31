#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    HOST = "127.0.0.1"
    PORT = 5010
    INSTANCE_URL = "http://127.0.0.1:5010"
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    ADMIN_EMAIL = "info@cases.lu"
    ADMIN_URL = "https://www.cases.lu"

    SECRET_KEY = ""

    LOG_PATH = "./var/stats.log"


class ProductionConfig(Config):
    DB_CONFIG_DICT = {
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": 5432,
    }

    DATABASE_NAME = "opendata"
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
        name=DATABASE_NAME, **DB_CONFIG_DICT
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
