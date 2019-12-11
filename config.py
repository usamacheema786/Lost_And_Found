import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = 'abc745588@gmail.com'

    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = True
    MAIL_USERNAME = 'abc745588@gmail.com'
    MAIL_PASSWORD = 'muslim123'

    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@mysql:3306/found_lost'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    CELERY_BROKER_URL = 'redis://redis:6379/0',
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


class DevelopmentConfig(Config):
    DEBUG = True
#
class TestingConfig(Config):
    TESTING = True

