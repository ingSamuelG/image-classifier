import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or  '07479fa1-a858-4f66-bb0c-5f8cfc0a1ae6'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def init_app(app):
        pass

class DevelopmentConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'data-dev.sqlite')

class TestingConfig(Config):
    debug = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'dataTest.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(base_dir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        try:
            from werkzeug.middleware.proxy_fix import ProxyFix
        except ImportError:
            print(ImportError)

config = { 
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}


