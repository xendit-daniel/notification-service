import os
from dotenv import load_dotenv

load_dotenv()

postgres_local_base = os.environ['DATABASE_URL']

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '\xf0\xd7A\x8an\xf2\xb1\x8aB\xba\x12\xdb\x05G\x08k6\xd9\x1d\xb7\x1b\x1c/\xd2')
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY