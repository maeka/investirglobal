# This Python file uses the following encoding: utf-8
import os, array
from app import app
from flask import Flask, Blueprint, make_response, render_template, redirect, flash, request, url_for, abort, send_from_directory
from werkzeug import url_encode
import requests
import json
import urllib
from app.models.forms import GetLead, DoLogin, InsertUser
from app.models.tables import User, Post, CatsTags, ZipperPostsCatsTags
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from is_safe_url import is_safe_url
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import psycopg2

from app import db

'''@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)'''




@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')


@app.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/webapp')
def webapp():
#category scheme
    cats = CatsTags.query.all()
    catag_id = []
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_id_ = CatsTags.query.filter_by(id=cat.id).first().id
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_id.append(catag_id_)
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme
    return render_template('pages/wpa.html',
                           title='Investir Global PWA',
                           catag_name=catag_name,
                           catag_colour=catag_colour,
                           len_cats = len(catag_name))


@app.route('/', defaults={'user': None})
@app.route('/index', defaults={'user': None})
@app.route('/index.html', defaults={'user': None})
def index(user):
    """Serve homepage template."""
#category scheme
    cats = CatsTags.query.all()
    catag_id = []
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_id_ = CatsTags.query.filter_by(id=cat.id).first().id
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_id.append(catag_id_)
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme

    #https://stackoverflow.com/questions/15791760/how-can-i-do-multiple-order-by-in-flask-sqlalchemy
    #posts = Post.query.order_by(Post.created_at.desc()).all()

    from sqlalchemy import text
    sql = text('''SELECT
    posts.id as id,
    posts.title as title,
    usr.name as author,
    datetime(posts.created_at) as pbdate,
    posts.image_thumb as img_thumb,
    group_concat(distinct ct.catag_name) as cats
    FROM posts AS posts
    LEFT JOIN zipper_posts_catstags AS zp ON posts.id = zp.post_id
    LEFT JOIN users AS usr ON posts.user_id = usr.id
    LEFT JOIN catstags AS ct ON zp.catag_id = ct.id
    GROUP BY 1, 2, 3, 4
    ORDER BY posts.created_at DESC;''')
    result = db.engine.execute(sql)
    posts_data = [row for row in result]

    return render_template("pages/index.html",
        posts_data = posts_data,
        catag_name=catag_name,
        catag_colour=catag_colour,
        len_cats = len(catag_name),
        user=user)


@app.route('/topic', defaults={'topic': None})
@app.route('/topic/<topic>')
def topic(topic):
#category scheme
    cats = CatsTags.query.all()
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme

    topic_row = CatsTags.query.filter_by(catag_name=topic).first()
    topic_id = topic_row.id
    topic_name = topic_row.catag_name
    print(topic_name)

    topic_posts_id = ZipperPostsCatsTags.query.filter_by(catag_id=topic_id).all()

    content_id = []
    content_title = []
    content_desc = []
    content_author = []
    content_body = []
    created_at = []
    image_featured = []
    image_thumb = []

    for post_id in topic_posts_id:
        content_id_ = Post.query.filter_by(id=post_id.post_id).first().id
        content_title_ = Post.query.filter_by(id=post_id.post_id).first().title
        content_desc_ = Post.query.filter_by(id=post_id.post_id).first().description
        print(Post.query.filter_by(id=post_id.post_id).first().user_id)
        content_author_ = User.query.filter_by(id=Post.query.filter_by(id=post_id.post_id).first().user_id).first().name
        content_body_ = Post.query.filter_by(id=post_id.post_id).first().content.encode("utf-8")
        created_at_ = Post.query.filter_by(id=post_id.post_id).first().created_at
        image_featured_ = Post.query.filter_by(id=post_id.post_id).first().image_featured
        image_thumb_ = Post.query.filter_by(id=post_id.post_id).first().image_thumb
        content_id.append(content_id_)
        content_title.append(content_title_)
        content_desc.append(content_desc_)
        content_author.append(content_author_)
        content_body.append(content_body_)
        created_at.append(created_at_)
        image_featured.append(image_featured_)
        image_thumb.append(image_thumb_)

    """Serve homepage template."""
    return render_template("pages/topic.html", 
        topic=topic_name, 
        content_id = content_id,
        content_title=content_title,
        content_author=content_author,
        content_desc=content_desc,
        content_body=content_body,
        created_at=created_at,
        len = len(topic_posts_id), 
        catag_name=catag_name, 
        catag_colour=catag_colour, 
        len_cats = len(catag_name),
        image_featured = image_featured,
        image_thumb = image_thumb
        )



@app.route('/content', defaults={'id': None, 'uri': None})
@app.route('/content/<int:id>')
def _content(id):
#category scheme
    cats = CatsTags.query.all()
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
    
    catag_name_str = ', '.join(catag_name)
    catag_name_str_query = ''.join(catag_name)
    #category scheme

    """Serve homepage template."""
    post = Post.query.filter_by(id=id).first()
    content_title = post.title
    content_author = User.query.filter_by(id=post.user_id).first()
    content_body = post.content 
    created_at = post.created_at
    topic_id = ZipperPostsCatsTags.query.filter_by(post_id=post.id).all()
    topic_name = []
    for id_topic in topic_id:
        topic_id_ = id_topic.catag_id
        topic_name_ = CatsTags.query.filter_by(id=id_topic.catag_id).first().catag_name
        topic_name.append(topic_name_)

    topic_name_str = "','".join(topic_name)
    topic_name_str_ = "'"+topic_name_str+"'"

    sql_raca_a = '''SELECT 
        posts.id as id, 
        posts.title as title, 
        usr.username as author,
        datetime(posts.created_at) as pbdate,
        posts.image_thumb as img_thumb, 
        group_concat(distinct ct.catag_name) as cats 
        FROM posts AS posts 
        LEFT JOIN zipper_posts_catstags AS zp ON posts.id = zp.post_id 
        LEFT JOIN users AS usr ON posts.user_id = usr.id 
        LEFT JOIN catstags AS ct ON zp.catag_id = ct.id 
        WHERE ct.catag_name IN ('''
    sql_raca_b = topic_name_str_
    sql_raca_c = ''')
        GROUP BY 1, 2, 3, 4 
        ORDER BY posts.created_at DESC;'''

    #print(sql_raca_a+sql_raca_b+sql_raca_c)

    sql_forza = sql_raca_a+sql_raca_b+sql_raca_c

    '''
    from sqlalchemy import text
    sql = text('''
    '''SELECT 
        posts.id as id, 
        posts.title as title, 
        usr.username as author,
        datetime(posts.created_at) as pbdate,
        posts.image_thumb as img_thumb, 
        group_concat(distinct ct.catag_name) as cats 
        FROM posts AS posts 
        LEFT JOIN zipper_posts_catstags AS zp ON posts.id = zp.post_id 
        LEFT JOIN users AS usr ON posts.user_id = usr.id 
        LEFT JOIN catstags AS ct ON zp.catag_id = ct.id 
        WHERE ct.catag_name IN (:x) 
        GROUP BY 1, 2, 3, 4 ORDER BY posts.created_at DESC;'''
        #)'''
    #print(sql)

    result = db.engine.execute(sql_forza)

    #result = db.engine.execute(sql, 
    #    x = topic_name[0])

    #result = db.engine.execute(sql, 
    #    x = "'"+topic_name_str+"'")
    #print(sql)

    posts_data = [row for row in result]


    #return content.title
    return render_template("pages/content.html", 
        id=id, 
        title=content_title, 
        author=content_author.name, 
        created_at=created_at, 
        content_body=content_body, 
        catag_name=catag_name, 
        topic_name = topic_name,
        len_topic_name = len(topic_name),
        catag_colour=catag_colour, 
        len_cats = len(catag_name),
        posts_data = posts_data)


@app.route('/test', defaults={'name': None})
@app.route('/test/<name>')
def test(name):
    """Serve homepage template."""
    if name:
        return 'Olá, %s!' % name
    else:
        return 'Olá usuário'


@app.route('/authors')
@app.route('/autores')
@app.route('/equipe')
def authors():
#category scheme
    cats = CatsTags.query.all()
    catag_id = []
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_id_ = CatsTags.query.filter_by(id=cat.id).first().id
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_id.append(catag_id_)
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme

    authors = User.query.filter_by(role='author').all()
    print(authors)
    return render_template("pages/authors.html",
        catag_name=catag_name,
        catag_colour=catag_colour,
        len_cats = len(catag_name),
        authors=authors)

@app.route('/author', defaults={'name': None})
@app.route('/author/<name>')
def author(name):
#category scheme
    cats = CatsTags.query.all()
    catag_id = []
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_id_ = CatsTags.query.filter_by(id=cat.id).first().id
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_id.append(catag_id_)
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme
    #author = User.query.filter_by(name=name).first()
    sql_author_role = User.query.filter_by(name=name).first().role
    sql_author_b = User.query.filter_by(name=name).first().username
    sql_author_a = '''SELECT
    posts.id as id,
    posts.title as title,
    usr.name as author,
    usr.description as description,
    usr.image_thumb as img,
    posts.created_at as pbdate,
    posts.image_thumb as img_thumb,
    group_concat(distinct ct.catag_name) as cats
    FROM posts AS posts
    LEFT JOIN zipper_posts_catstags AS zp ON posts.id = zp.post_id
    LEFT JOIN users AS usr ON posts.user_id = usr.id
    LEFT JOIN catstags AS ct ON zp.catag_id = ct.id
    WHERE usr.username LIKE "''' 
    str(sql_author_b)
    sql_author_c = '''" ORDER BY posts.created_at DESC;'''

    sql_author = sql_author_a+sql_author_b+sql_author_c
    print(sql_author)

    result = db.engine.execute(sql_author)

    author_data = [row for row in result]

    #return "author"+ name

    if sql_author_role == 'author':
        return render_template("pages/author.html",
        catag_name=catag_name,
        catag_colour=catag_colour,
        len_cats = len(catag_id),
        len = len(author_data),
        author=author_data)




@app.route('/sobre')
@app.route('/about')
@app.route('/sobre.html')
def about():
#category scheme
    cats = CatsTags.query.all()
    catag_id = []
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_id_ = CatsTags.query.filter_by(id=cat.id).first().id
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_id.append(catag_id_)
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme

    return render_template("pages/about.html",
        catag_name=catag_name,
        catag_colour=catag_colour,
        len_cats = len(catag_name))


'''def redirect_dest(fallback):
    dest = request.args.get('next')
    if not is_safe_url(dest):
        return abort(400)
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)'''


@app.route('/login', methods=['POST', 'GET'])
@app.route('/login.html', methods=['POST', 'GET'])
@app.route('/login.html?next=index', methods=['POST', 'GET'])

def login():
    """Serve homepage template."""
#category scheme
    cats = CatsTags.query.all()
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme


    form = DoLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.rememberme.data)
            User.get_id(user)
            print(current_user)
            flash("Logged in!")
            #return redirect_dest(fallback=url_for('index', next=request.endpoint))
            if user.role == 'admin':
                next = 'admin'
            else:
                next = request.args.get('next')
            #next = 'index'
            print(next)
            if not is_safe_url(next, {"127.0.0.1:5000"}):
                return abort(400)
            return redirect(next) 
            #return redirect(next or url_for('index'))            
        else:
            flash("Invalid login.")
    else:
        print(form.errors)
    return render_template("forms/login.html", 
        form=form, 
        catag_name=catag_name, 
        catag_colour=catag_colour, 
        len_cats = len(catag_name))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['POST', 'GET'])
def register():
#category scheme
    cats = CatsTags.query.all()
    catag_name = []
    catag_colour = []
    for cat in cats:
        catag_name_ = CatsTags.query.filter_by(id=cat.id).first().catag_name
        catag_colour_ = CatsTags.query.filter_by(id=cat.id).first().catag_colour
        catag_name.append(catag_name_)
        catag_colour.append(catag_colour_)
#category scheme

    form = InsertUser()
    if form.validate_on_submit():
        i = User(form.data['name'], 
            form.data['username'],
            form.data['email'],
            form.data['password'],
            form.data['role'])
        db.session.add(i)
        db.session.commit()
        print('valido')
        return render_template('pages/index.html', 
            form=form, 
            catag_name=catag_name, 
            catag_colour=catag_colour, 
            len_cats = len(catag_name))
    else:
        print(form.errors)
    return render_template('forms/register.html', 
        form=form, 
        catag_name=catag_name, 
        catag_colour=catag_colour, 
        len_cats = len(catag_name))



@app.route("/reports")
@login_required
def reports():
    return "em breve!"
