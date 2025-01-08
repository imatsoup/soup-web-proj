from flask import render_template, url_for, request, redirect, session, flash, Blueprint
import bcrypt
from .blog import blog_read, blog_write
from pathlib import Path

from .extensions import db
from .models import users

main = Blueprint("main", __name__)

@main.route('/test')
def test():
    return '<h1>Test</h1>'

@main.route('/', methods=['POST', 'GET'])
@main.route('/home', methods=['POST', 'GET'])
def home():
    # IF METHOD POST, WRITE TO db
    if request.method == 'POST':
        blog_title = request.form['edit_blog_title']
        blog_con = request.form['edit_blog_content']
        blog_write(blog_title, blog_con)

    list = blog_read()

    return render_template('index.html', list = list)

@main.route('/create', methods=['POST', 'GET'])
def create():
    #IF METHOD POST, try to create account
    if request.method == 'POST':
        session.permanent = True
        uname = request.form['nm']
        pw = request.form['pw']
        uemail = request.form['email']
        name_found = users.query.filter_by(name=uname).first()
        email_found = users.query.filter_by(email=uemail).first()
        if name_found:
            flash('Username already in use', 'info')
            return redirect(url_for('main.create'))
        if email_found:
            flash('Email already in use!', 'info')
            return redirect(url_for('main.create'))
        else:
            bytes = pw.encode()
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt)
            new_usr = users(uname, uemail, hashed_password)
            db.session.add(new_usr)
            db.session.commit()
            flash('Account created!')
            return redirect(url_for('main.login'))
    else:
        session['user'] = None
        return render_template('create.html')
    
@main.route('/login', methods=['POST', 'GET'])
def login():
    #IF METHOD POST, try to login
        if request.method == 'POST':       
            uname = request.form['nm']
            pw = request.form['pw']
            found_user = users.query.filter_by(name=uname).first()
            if found_user and bcrypt.checkpw(pw.encode(), found_user.pw):
                session.permanent = True
                session['user'] = uname
                return redirect(url_for('main.home'))
            else: 
                flash('Your information was incorrect!', 'info')
                return redirect(url_for('main.login'))
        else:
            session['user'] = None
            return render_template('login.html')
        
@main.route('/rickroll')
def rickroll():
    #Just a funny joke
    return '<style>body{background-image: url("static/rickroll.gif");}</style>'

@main.route('/logout')
def logout():
    #If we hit this route, clear session vars
    flash('You have been logged out!', 'info')
    session.pop('user', None)
    return redirect(url_for('main.login'))

