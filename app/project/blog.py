from .extensions import db
from .models import blogposts
from sqlalchemy import desc
import datetime
def blog_read():
    blog_list = []
    for entry in blogposts.query.order_by(desc(blogposts.date)).all():
        blog_list.append(entry.content)
    return blog_list

def blog_write(con):
    cur_date = datetime.datetime.now()
    new_entry = blogposts(con, cur_date)
    db.session.add(new_entry)
    db.session.commit() 