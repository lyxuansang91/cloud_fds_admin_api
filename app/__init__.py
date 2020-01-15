import datetime
import json
import os
from logging import INFO, Formatter, handlers

from bson import ObjectId
from flask import Flask
from werkzeug.exceptions import default_exceptions

from .errors.handler import api_error_handler
from flask_cors import CORS
from .extensions import db, flask_bcrypt, jwt_manager, ma, mail


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def create_app(config_cls):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_cls)
    __init_app(app)
    __register_blueprint(app)
    __config_logging(app)
    __config_error_handlers(app)

    return app


def __config_logging(app):
    if not app.debug and not app.testing:
        fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        formatter = Formatter(fmt=fmt)

        info_log = os.path.join(app.config['LOG_FOLDER'], 'app.log')
        info_log_handler = handlers.RotatingFileHandler(
            filename=info_log,
            maxBytes=1024 ** 2,
            backupCount=10)
        info_log_handler.setLevel(level=INFO)
        info_log_handler.setFormatter(fmt=formatter)
        app.logger.addHandler(info_log_handler)

    app.logger.setLevel(INFO)
    app.logger.info('Start CLOUD FDS ADMIN API...')


def __register_blueprint(app):
    from app.api import bp as api_bp
    app.register_blueprint(api_bp)


def __init_app(app):
    ma.init_app(app)
    flask_bcrypt.init_app(app)
    jwt_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)


def __config_error_handlers(app):
    for exp in default_exceptions:
        app.register_error_handler(exp, api_error_handler)
    app.register_error_handler(Exception, api_error_handler)
