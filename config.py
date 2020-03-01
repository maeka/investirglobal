import os.path
from flask_sslify import SSLify


basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
HOST = '0.0.0.0'
PORT = 8080
#SSL_CONTEXT = 'adhoc'

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'keyhole'
