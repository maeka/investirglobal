from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_user, LoginManager, current_user, login_required, logout_user
from flask_admin import Admin, BaseView, expose, AdminIndexView
import os
from flask_sslify import SSLify



app = Flask(__name__, 
	instance_relative_config=True,
	static_url_path='')
app.config.from_object('config')


if 'DYNO' in os.environ:
	sslify = SSLify(app)  # only trigger SSLify if the app is running on Heroku


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)


from app.models import tables 
from app.controllers import default


#return app