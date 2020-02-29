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
	description = db.Column(db.String)
	image_thumb = db.Column(db.String)

	def __init__(self, name, username, email, password, role, description, image_thumb):
		self.name = name
		self.username = username
		self.email = email
		self.password = password
		self.role = role
		self.description = description
		self.image_thumb = image_thumb

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
	uri = db.Column(db.Text, unique=True)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	image_featured = db.Column(db.Text)
	image_thumb = db.Column(db.Text)
	image_thumb_mini = db.Column(db.Text)

	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

	user = db.relationship('User', foreign_keys=user_id)

	def __init__(self, title, description, content, uri, created_at, updated_at, user_id, image_featured, image_thumb, image_thumb_mini):
		self.title = title
		self.description = description
		self.content = content
		self.uri = uri
		self.created_at = created_at
		self.updated_at = created_at
		self.user_id = user_id
		self.image_featured = image_featured
		self.image_thumb = image_thumb
		self.image_thumb_mini = image_thumb_mini


	@property
	def get_content(id):
		return Post.query.filter_by(id=id).first()

	@property
	def get_title(id):
		post = Post.query.filter_by(id=id).first()
		print(post)


	def __repr__(self):
		return '<Post %r>' % self.title



class Follow(db.Model):
	__tablename__ = "follow"

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	follower_id = db .Column(db.Integer, db.ForeignKey('users.id'))

	user = db.relationship('User', foreign_keys=user_id)
	follower = db.relationship('User', foreign_keys=follower_id)

	def __init__(self, user_id, follower_id):
		self.user_id = user_id
		self.follower_id = follower_id


class CatsTags(db.Model):
	__tablename__ = "catstags"

	id = db.Column(db.Integer, primary_key=True)
	catag_name = db.Column(db.Text)
	catag_parent_id = db .Column(db.Integer, db.ForeignKey('catstags.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	catag_colour = db.Column(db.Text)

	user = db.relationship('User', foreign_keys=user_id)
	parent = db.relationship('CatsTags', foreign_keys=catag_parent_id)

	def __init__(self, catag_name, catag_parent_id, user_id, catag_colour):
		self.catag_name = catag_name
		self.catag_parent_id = catag_parent_id
		self.user_id = user_id
		self.catag_colour = catag_colour

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

	def __repr__(self):
		return '<ZipperPostsCatsTags %r>' % int(self.id)
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

