from app import db
from app.mixins import CRUDMixin
from flask.ext.login import UserMixin
from app.tracking.models import Site

class User(UserMixin, CRUDMixin,  db.Model):
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    sites = db.relationship('Site', backref='site',
                                lazy='dynamic')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)