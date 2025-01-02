from .extensions import db

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    pw = db.Column(db.String(100))

    def __init__(self, name, email, pw):
        self.name = name
        self.email = email
        self.pw = pw