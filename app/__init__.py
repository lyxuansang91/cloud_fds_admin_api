import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from werkzeug.exceptions import default_exceptions

from .errors.handler import api_error_handler
from .extensions import flask_bcrypt, jwt_manager, ma, mongo


def create_app(config_cls):
    app = Flask(__name__)
    app.config.from_object(config_cls)
    __init_app(app)
    __register_blueprint(app)
    __config_logging(app)
    __config_error_handlers(app)

    return app


def __config_logging(app):
    if not app.debug and not app.testing:
        app_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(app_dir)
        logs_dir = os.path.join(root_dir, 'logs')
        if not os.path.exists(os.path.join(root_dir, 'logs')):
            os.mkdir(os.path.join(root_dir, 'logs'))
        file_handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'),
                                           maxBytes=1024**2,
                                           backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                              '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Start CLOUD FDS ADMIN API...')


def __register_blueprint(app):
    from app.api import bp as api_bp
    app.register_blueprint(api_bp)


def __init_app(app):
    ma.init_app(app)
    mongo.init_app(app)
    flask_bcrypt.init_app(app)
    jwt_manager.init_app(app)


def __config_error_handlers(app):
    for exp in default_exceptions:
        app.register_error_handler(exp, api_error_handler)
    app.register_error_handler(Exception, api_error_handler)
