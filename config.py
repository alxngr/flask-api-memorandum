import os
import logging
import pathlib


class Config:
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    UPLOADED_IMAGES_DEST = 'static/images'

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 600

    RATELIMIT_HEADERS_ENABLED = True

    ROOT = pathlib.Path(__file__).resolve().parent
    LOG_DIR = ROOT / 'logs'
    LOG_DIR.mkdir(exist_ok=True)
    LOG_FILE = LOG_DIR / 'api.log'
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_DBNAME = 'your-db-name'
    SQLALCHEMY_DATABASE_USERNAME = 'your-db-username'
    SQLALCHEMY_DATABASE_PASSWORD = 'your-db-password'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{SQLALCHEMY_DATABASE_USERNAME}:{SQLALCHEMY_DATABASE_PASSWORD}@localhost/{SQLALCHEMY_DATABASE_DBNAME}'

    SECRET_KEY = 'secret-key'


class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
