# This Python file uses the following encoding: utf-8
from app import db, app, login_manager
from flask_login import UserMixin, login_user, LoginManager, current_user, login_required, logout_user
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, redirect, flash, request, url_for, abort

class User(db.Model):
	__tablename__= "users"


	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	role = db.Column(db.String)

	def __init__(self, name, username, email, password, role):
		self.name = name
		self.username = username
		self.email = email
		self.password = password
		self.role = role

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonimous(self):
		return False

	def get_id(self):
		return str(self.id)

	@login_manager.user_loader
	def load_user(user_id):
		try:
			return User.query.get(user_id)
		except:
			return None

	def __repr__(self):
		return '<User %r>' % self.username



class Post(db.Model):
	__tablename__ = "posts"


	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	description = db.Column(db.Text)
	content = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

	user = db.relationship('User', foreign_keys=user_id)

	def __init__(self, title, description, content, created_at, updated_at, user_id):
		self.title = title
		self.description = description
		self.content = content
		self.created_at = created_at
		self.updated_at = created_at
		self.user_id = user_id

	def __repr__(self):
		return '<Post %r>' % self.id



class Follow(db.Model):
	__tablename__ = "follow"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	follower_id = db .Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User', foreign_keys=user_id)
	follower = db.relationship('User', foreign_keys=follower_id)


class CatsTags(db.Model):
	__tablename__ = "catstags"

	id = db.Column(db.Integer, primary_key=True)
	catag_name = db.Column(db.Text)
	catag_parent_id = db .Column(db.Integer, db.ForeignKey('catstags.id'))
	
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User', foreign_keys=user_id)
	parent = db.relationship('CatsTags', foreign_keys=catag_parent_id)

	def __repr__(self):
		return '<CatsTags %r>' % self.catag_name


class ZipperPostsCatsTags(db.Model):
	__tablename__ = "zipper_posts_catstags"

	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	catag_id = db .Column(db.Integer, db.ForeignKey('catstags.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User', foreign_keys=user_id)
	post = db.relationship('Post', foreign_keys=post_id)
	cattag = db.relationship('CatsTags', foreign_keys=catag_id)


#admin = Admin(app, index_view=MyAdminIndexView())

# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()

flask_admin = Admin(app, index_view=MyAdminIndexView())

flask_admin.add_view(ModelView(User, db.session))
flask_admin.add_view(ModelView(Post, db.session))
flask_admin.add_view(ModelView(Follow, db.session))
flask_admin.add_view(ModelView(CatsTags, db.session))
flask_admin.add_view(ModelView(ZipperPostsCatsTags, db.session))

