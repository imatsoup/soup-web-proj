from flask import Flask
from datetime import timedelta
from .extensions import db
from .models import users
from .routes import main

def create_app(database_uri=''):
    app = Flask(__name__)
    app.secret_key = 'anuvs5flz13zlnsat1'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.permanent_session_lifetime = timedelta(minutes=5)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.register_blueprint(main)
    
    return app
    