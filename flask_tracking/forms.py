from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Site


class SiteForm(Form):
    base_url = fields.StringField()


class VisitForm(Form):
    browser = fields.StringField()
    date = fields.DateField()
    event = fields.StringField()
    url = fields.StringField()
    ip_address = fields.StringField("IP Address")
    site = QuerySelectField(query_factory=lambda: Site.query.all())
