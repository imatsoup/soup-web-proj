from flask import render_template, url_for, request, redirect, session, flash, Blueprint
import bcrypt
from pathlib import Path

from .extensions import db
from .models import users

main = Blueprint("main", __name__)

@main.route('/')
def test():
    return '<h1>Test</h1>'

@main.route('/home', methods=['POST', 'GET'])
def home():
    # IF METHOD POST, WRITE TO FILE, then do the rest and display our new text
    filepath= Path('text.txt')
    
    if request.method == 'POST':
        blog = request.form['text_box']
        with open(filepath, 'w') as f:
            f.write(blog)
    
    text = 'Default'
    if filepath.is_file():
        with open(filepath, 'r') as f:
            text = f.read();

    return render_template('index.html', text = text)
@main.route('/create', methods=['POST', 'GET'])
def create():
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
        return render_template('create.html')
@main.route('/login', methods=['POST', 'GET'])
def login():
        if request.method == 'POST':       
            uname = request.form['nm']
            pw = request.form['pw']
            found_user = users.query.filter_by(name=uname).first()
            if found_user and bcrypt.checkpw(pw.encode(), found_user.pw):
                session.permanent = True
                session['user'] = uname
                flash('Identity confirmed', 'info')
                return redirect(url_for('main.home'))
            else: 
                flash('Your information was incorrect!', 'info')
                return redirect(url_for('main.login'))
        else:
            return render_template('login.html')
@main.route('/logout')
def logout():
    flash('You have been logged out!', 'info')
    session.pop('user', None)
    return redirect(url_for('main.login'))