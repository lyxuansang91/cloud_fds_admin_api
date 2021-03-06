import os
import datetime


root_app = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def _make_dir(dir_name):
    """ Make folder used to store log files. """

    log_dir_path = os.path.join(root_app, dir_name)
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    return log_dir_path


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something-very-secret'
    API_URL = os.environ.get('API_URL') or 'http://localhost:5000'
    MONGODB_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGO_PASSWORD')
    LOG_FOLDER = _make_dir('logs')
    MONGODB_HOST = os.environ.get('MONGO_HOST') or 'localhost'
    MONGODB_PORT = int(os.environ.get('MONGO_PORT')) or 27017
    MONGODB_DB = os.environ.get('MONGO_DATABASE') or 'cloudFDS'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=2)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT')) or 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LOGIN_URL = os.environ.get('LOGIN_URL') or 'http://localhost:3000/login'
    RESET_PASSWORD_URL = os.environ.get('RESET_PASSWORD_URL') or 'http://localhost:3000/reset-password'
    MAXIMUM_USER_API = 3


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


configs = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
