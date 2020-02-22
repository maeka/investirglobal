from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug import url_encode


class GetLead(FlaskForm):
	email = StringField('Email address', validators=[DataRequired(),Email()])

class DoLogin(FlaskForm):
	#name = StringField('name', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	#email = StringField('e-mail', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	rememberme = BooleanField('lembre-me')

class AdminLogin(FlaskForm):
    #name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    #email = StringField('e-mail', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    rememberme = BooleanField('lembre-me')

'''
class InsertUser(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	username = StringField('username', validators=[DataRequired()])
	email = StringField('e-mail', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	'''


class InsertUser(FlaskForm):
    name = TextField(
        'Name', validators=[DataRequired(), Length(min=5, max=25)]
    )
    username = StringField(
    	'username', validators=[DataRequired()]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    role = HiddenField(
        'Role'
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


