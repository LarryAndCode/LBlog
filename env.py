import os

HOST = '127.0.0.1'
PORT = 5000
DEBUG = True
APP_PATH = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + APP_PATH + '/tmp/lblog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

USERNAME = '1'
PASSWORD = '1'
SECRET_KEY = '7c401a1e5fd54c6cd8cd0d5016c2911157a6127815ab76'

PICTURENUM = 1


