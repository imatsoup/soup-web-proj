from flask import render_template, url_for, request, redirect, session, flash, Blueprint
import bcrypt
from .blog import blog_read, blog_write
from.account import a_create, a_login

from .models import users

main = Blueprint("main", __name__)

# route to test the server is running
@main.route('/test')
def test():
    return '<h1>Test</h1>'

# Home page route
@main.route('/', methods=['POST', 'GET'])
@main.route('/home', methods=['POST', 'GET'])
def home():
    # IF METHOD POST, WRITE new post TO db
    if request.method == 'POST':
        blog_title = request.form['edit_blog_title']
        blog_con = request.form['edit_blog_content']
        blog_write(blog_title, blog_con)

    list = blog_read()

    return render_template('index.html', list = list)

@main.route('/blogpost/<title>/<content>')
def blogpost(title, content):
    return render_template('blogpost.html', title=title, content=content)

# Account creation page route
@main.route('/create', methods=['POST', 'GET'])
def create():
    #IF METHOD POST, try to create account
    if request.method == 'POST':
        session.permanent = True
        uname = request.form['nm']
        if uname == '':
            flash('Username required!')         
        pw = request.form['pw']
        uemail = request.form['email']
        # Check the result of our attempt to create an account, then act accordingly
        result = a_create(uname, uemail, pw)
        if result == -2:
            flash('Invalid username!', 'info')
            return redirect(url_for('main.create'))
        if result == -1:
            flash('Invalid password!', 'info')
            return redirect(url_for('main.create'))
        if result == 0:
            flash('Username already in use', 'info')
            return redirect(url_for('main.create'))
        if result == 1:
            flash('Email already in use!', 'info')
            return redirect(url_for('main.create'))
        else:
            flash('Account created!')
            return redirect(url_for('main.login'))
    else:
        session['user'] = None
        return render_template('create.html')

# Login page route    
@main.route('/login', methods=['POST', 'GET'])
def login():
    #IF METHOD POST, try to login
        if request.method == 'POST':       
            uname = request.form['nm']
            pw = request.form['pw']
            result = a_login(uname, pw)
            # Depending on result of login attempt, update session or show error message and refresh
            if result:
                session.permanent = True
                session['user'] = uname
                return redirect(url_for('main.home'))
            else: 
                flash('Your information was incorrect!', 'info')
                return redirect(url_for('main.login'))
        else:
            session['user'] = None
            return render_template('login.html')

# Funny Joke^tm        
@main.route('/rickroll')
def rickroll():
    #Just a funny joke
    return '<style>body{background-image: url("static/rickroll.gif");}</style>'

# Account Logout Route
@main.route('/logout')
def logout():
    #If we hit this route, clear session vars
    flash('You have been logged out!', 'info')
    session.pop('user', None)
    return redirect(url_for('main.login'))

@main.errorhandler(404)
def page_not_found():
    return 'Page Not Found'

@main.errorhandler(500)
def error():
    return 'Failed to connect to database'