from app import db
from app.mixins import CRUDMixin

class Site(CRUDMixin, db.Model):
    __tablename__ = 'tracking_site'
    id = db.Column(db.Integer, primary_key=True)
    visits = db.relationship('Visit', backref='tracking_site',
                                lazy='select')
    base_url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))


    def __init__(self, user_id=None, base_url=None):
        self.user_id = user_id
        self.base_url = base_url

    def __repr__(self):
        return '<Site %r>' % (self.base_url)


class Visit(CRUDMixin, db.Model):
    __tablename__ = 'tracking_visit'
    id = db.Column(db.Integer, primary_key=True)
    browser = db.Column(db.Text)
    date = db.Column(db.DateTime)
    event = db.Column(db.Text)
    url = db.Column(db.Text)
    site_id = db.Column(db.Integer, db.ForeignKey('tracking_site.id'))
    ip_address = db.Column(db.Text)
    location = db.Column(db.Text)
    location_full = db.Column(db.Text)

    def __init__(self, browser=None, date=None, event=None, url=None, ip_address=None, location_full=None, location=None):
        self.browser = browser
        self.date = date
        self.event = event
        self.url = url
        self.ip_address = ip_address
        self.location_full = location_full

    def __repr__(self):
        return '<Visit %r - %r>' % (self.url, self.date)