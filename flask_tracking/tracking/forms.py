from datetime import datetime as dt

from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Site


class SiteForm(Form):
    base_url = fields.StringField(validators=[Required()])


class VisitForm(Form):
    browser = fields.StringField()
    date = fields.DateField(default=dt.now)
    event = fields.StringField()
    url = fields.StringField(validators=[Required()])
    ip_address = fields.StringField()
    location = fields.StringField()
    latitude = fields.StringField()
    longitude = fields.StringField()
    site = QuerySelectField(validators=[Required()], query_factory=lambda: Site.query.all())
