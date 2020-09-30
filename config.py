import os

class Config:
    POSTS_PER_PAGE = 3
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOADED_PHOTOS_DEST ='app/static/img'

    #  email configurations

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wainainakasyoka:W41n41n4@localhost/dailyblog_test'
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wainainakasyoka:W41n41n4@localhost/dailyblog'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig

}