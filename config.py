import os.path

basedir = 'https://'+os.path.abspath(os.path.dirname(__file__))

DEBUG = True
HOST = "0.0.0.0"
PORT = 8080

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'keyhole'

