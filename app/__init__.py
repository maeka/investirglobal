from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_user, LoginManager, current_user, login_required, logout_user
from flask_admin import Admin, BaseView, expose, AdminIndexView
import os
from flask import request, redirect
from flask_talisman import Talisman
from flask_ckeditor import CKEditor, CKEditorField


app = Flask(__name__)
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        '*.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'storage.googleapis.com',
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        '*.w3.org',
        '*.youtube.com',
        'storage.googleapis.com',
        's.ytimg.com',
        '*.github.com',
        '*.cloudflare.com',
        'cdn.ckeditor.com'
    ],
    'img-src': [
        '\'self\' data:',
        '\'unsafe-inline\'',
        '*.bootstrapcdn.com',
        '*.w3.org',
        '*.github.com',
        '*.cloudflare.com',
        'cdn.ckeditor.com'
    ],
    'media-src': [
            '*',
    ],
    'object-src data': [
        '\'unsafe-eval\''
    ],
    'style-src': [
    '\'unsafe-inline\' \'self\'',
    '*.bootstrapcdn.com',
    'code.jquery.com',
    'cdn.jsdelivr.net',
    'storage.googleapis.com',
    'fonts.googleapis.com',
    'fonts.gstatic.com',
    'cdnjs.cloudflare.com',
    'cdn.ckeditor.com'
    ],
    'script-src': [
    '\'unsafe-inline\' \'self\'',
    '*.bootstrapcdn.com',
    'code.jquery.com',
    'cdn.jsdelivr.net',
    'storage.googleapis.com',
    'fonts.googleapis.com',
    'fonts.gstatic.com',
    '*.cloudflare.com',
    'cdn.ckeditor.com']
}

Talisman(app, content_security_policy=csp)

'''@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)'''

#if 'DYNO' in os.environ:
	#sslify = SSLify(app, permanent=True)  # only trigger SSLify if the app is running on Heroku
	#print(sslify)

app.config.from_object('config')





db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

ckeditor = CKEditor(app)

from app.models import tables 
from app.controllers import default


#return app