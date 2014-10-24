import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECURET_KET = os.environ.get('SECRET_KEY') or 'chuangxin chuangye xiangmu'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SUBJECT_PREFIX = '[************************]'
    FLASK_MAIL_SENDER = 'Ligulf Zhou<ligulfzhou53@gmail.com>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zhouligang@localhost/flask_restaurant_develop'


class TestingConfig(Config):
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or\
    #    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zhouligang@localhost/flask_restaurant_test'


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:zhouligang@localhost/flask_restaurant'

config = {
    'development'   : DevelopmentConfig,
    'testing'       : TestingConfig,
    'production'    : ProductionConfig,

    'default'       : DevelopmentConfig
}
