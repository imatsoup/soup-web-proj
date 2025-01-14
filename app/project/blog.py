from .extensions import db
from .models import blogposts
from sqlalchemy import desc
import datetime
# Read available blog entries from the db
def blog_read():
    blog_list = []
    for entry in blogposts.query.order_by(desc(blogposts.date)).all():
        blog_list.append(entry)
    return blog_list

# Check input validity, and if valid, enter new entry into db and commit
def blog_write(title, con):
    if title != '' and con != '':
        cur_date = datetime.datetime.now()
        new_entry = blogposts(title, con, cur_date)
        db.session.add(new_entry)
        db.session.commit()