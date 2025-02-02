from .extensions import db
import datetime

# Table for user accounts
class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    pw = db.Column(db.String(100))

    def __init__(self, name, email, pw):
        self.name = name
        self.email = email
        self.pw = pw

# Table for blogposts        
class blogposts(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    title = db.Column(db.String(100))
    content = db.Column(db.Text())
    
    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date