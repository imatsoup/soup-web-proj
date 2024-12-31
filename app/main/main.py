from flask import Flask, render_template, url_for, request, redirect, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from pathlib import Path
import sys


app = Flask(__name__)
app.secret_key = "anuvs5flz13zlnsat1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    pw = db.Column(db.String(100))

    def __init__(self, name, email, pw):
        self.name = name
        self.email = email
        self.pw = pw

@app.route("/")
def test():
    return "<h1>Test</h1>"

@app.route("/home", methods=["POST", "GET"])
def home():
    # IF METHOD POST, WRITE TO FILE, then do the rest and display our new text
    filepath= Path('text.txt')
    text = "Default"
    if filepath.is_file():
        with open('text.txt', 'r') as f:
            text = f.read();
    # blog = request.form["text"]
    return render_template("index.html", text = text)
@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        session.permanent = True
        uname = request.form["nm"]
        pw = request.form["pw"]
        uemail = request.form["email"]
        name_found = users.query.filter_by(name=uname).first()
        email_found = users.query.filter_by(email=uemail).first()
        if name_found:
            flash("Username already in use", "info")
            return redirect(url_for("create"))
        if email_found:
            flash("Email already in use!", "info")
            return redirect(url_for("create"))
        else:
            bytes = pw.encode()
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt)
            new_usr = users(uname, uemail, hashed_password)
            db.session.add(new_usr)
            db.session.commit()
            flash("Account created!")
            return redirect(url_for("login"))
    else:
        return render_template("create.html")
@app.route("/login", methods=["POST", "GET"])
def login():
        if request.method == "POST":       
            uname = request.form["nm"]
            pw = request.form["pw"]
            found_user = users.query.filter_by(name=uname).first()
            if found_user and bcrypt.checkpw(pw.encode(), found_user.pw):
                session.permanent = True
                session["user"] = uname
                flash("Identity confirmed", "info")
                return redirect(url_for("home"))
            else: 
                flash("Your information was incorrect!", "info")
                return redirect(url_for("login"))
        else:
            return render_template("login.html")
@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin_pw = '123'
        bytes = admin_pw.encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes, salt)
        db.session.add(users('admin', 'asf@gmail.com', hashed_password))
        db.session.commit
    app.run(debug=True)