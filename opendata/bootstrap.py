#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import io
from typing import Any
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, format_datetime
from flask_migrate import Migrate


def set_logging(
    log_path=None,
    log_level=logging.INFO,
    modules=(),
    log_format="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)s: %(message)s",
):
    if not modules:
        modules = (
            "root",
            "runserver",
            "opendata.api.v1.client",
            "opendata.commands.stats",
        )
    handler = io.BytesIO()  # type: Any
    if log_path:
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        if not os.path.exists(log_path):
            open(log_path, "w").close()
        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler()
    formater = logging.Formatter(log_format)
    handler.setFormatter(formater)
    for logger_name in modules:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        for handler in logger.handlers:
            handler.setLevel(log_level)
        logger.setLevel(log_level)


# Create Flask application
application = Flask(__name__, instance_relative_config=True)

# Load the appropriate configuration
#ON_HEROKU = int(os.environ.get("HEROKU", 0)) == 1
TESTING = os.environ.get("testing", "") == "actions"
if TESTING:
    # Testing on GitHub Actions
    application.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://opendata:password@localhost:5432/statsservice"
# elif ON_HEROKU:
#     # if the application is running on Heroku
#     application.config.from_pyfile("heroku.py", silent=False)
#     application.config["INSTANCE_URL"] = os.environ.get("INSTANCE_URL", "")
elif os.environ.get("STATS_CONFIG", ""):
    # if a specific configuration is provided by the user
    # this does not works with mod_wsgi
    config_file = os.environ.get("STATS_CONFIG", "")
    application.config.from_pyfile(config_file, silent=False)
else:
    try:
        application.config.from_pyfile("production.py", silent=False)
    except Exception:
        # default configuration file
        application.config.from_object("instance.config.ProductionConfig")

# Set SECRET_KEY if it was not defined
if not application.config.get("SECRET_KEY", False):
    application.config["SECRET_KEY"] = os.urandom(24)

set_logging(application.config.get("LOG_PATH", None))

db = SQLAlchemy(application)
migrate = Migrate(application, db)

# Internationalization
babel = Babel(application)

application.jinja_env.filters["datetime"] = format_datetime


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    # user = getattr(g, 'user', None)
    # if user is not None:
    #     return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(["fr", "en"])
