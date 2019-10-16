from FlaskAPP import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return Mocklogin.query.get(int(user_id))


class Mocklogin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    last_login = db.Column(db.DateTime(datetime.datetime.now()))
