from .models import users
from .extensions import db
import re
import bcrypt

# Function for user account logging in by checking password and username against db records
def a_login(uname, pwd):
    found_user = users.query.filter_by(name=uname).first()
    if found_user and bcrypt.checkpw(pwd.encode(), found_user.pw):
            return True
    else:
        return False

# Function for creating a user account
def a_create(uname, email, pwd):
    # Input validation
    u_check = re.findall(' ', uname)
    p_check = re.findall(' ', pwd)
    # If either user email or password fail to validate, return fail conditions
    if len(u_check) != 0:
        return -2
    elif len(p_check) != 0:
        return -1
    # Else, check db for already existing user. If found, return fail results. If successful, commit to db and return success
    else:
        found_user = users.query.filter_by(name=uname).first()
        email_found = users.query.filter_by(email=email).first()
        if found_user:
            return 0
        elif email_found:
            return 1
        else:
            bytes = pwd.encode()
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt)
            new_usr = users(uname, email, hashed_password)
            db.session.add(new_usr)
            db.session.commit()
            return 2