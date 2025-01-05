from .extensions import db
import datetime

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    pw = db.Column(db.String(100))

    def __init__(self, name, email, pw):
        self.name = name
        self.email = email
        self.pw = pw
        
class blogposts(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.timezone.utc)
    content = db.Column(db.Text())
    
    def __init__(self, content, date):
        self.content = content
        self.date = date