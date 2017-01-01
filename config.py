import os

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '<huan_zhong2@126.com>'
    FLASKY_ANDMIN  = '13251183@bjtu.edu.cn'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER  = 'smtp.126.com'
    MAIL_PORT = 465
    MAIL_USE_SSL  = True
    MAIL_USERNAME  = 'huan_zhong2@126.com'
    MAIL_PASSWORD  = 'zh520596'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://johan:123456@localhost:3306/flightflowDev'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://johan:123456@localhost:3306/test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://johan:123456@localhost:3306/flightflow'

config = {
    'development' : DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}