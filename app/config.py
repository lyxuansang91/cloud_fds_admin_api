import os
import datetime
import urllib.parse

basedir = os.path.abspath(os.path.dirname(__file__))


def get_mongo_uri(username, password, host, port, database):
    if username is None and password is None:
        return f'mongodb://{host}:{port}/{database}'
    password = urllib.parse.quote_plus(password)
    return f'mongodb://{username}:' + password + f'@{host}:{port}/{database}?retryWrites=true'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something-very-secret'
    MONGODB_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGODB_HOST = os.environ.get('MONGO_HOST') or 'localhost'
    MONGODB_PORT = os.environ.get('MONGO_PORT') or 27017
    MONGODB_DB = os.environ.get('MONGO_DATABASE') or 'cloudFDS'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


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
