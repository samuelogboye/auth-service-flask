''' configuration file for the app'''
import os
from dotenv import load_dotenv

load_dotenv()

class Config: # pylint: disable=too-few-public-methods
    ''' Base Configuration for all environments '''
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')

class DevelopmentConfig(Config): # pylint: disable=too-few-public-methods
    ''' Base Configuration for Development environment '''
    DEBUG = True

class TestingConfig(Config):# pylint: disable=too-few-public-methods
    ''' Base Configuration for Testing environment '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# class ProductionConfig(Config):
#     ''' Base Configuration for Production environment '''
#     pass
