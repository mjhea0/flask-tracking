from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, RecaptchaField, fields, validators
from flask.ext.wtf import Required, Email, EqualTo
from app.users.models import User
from app import db

class RegisterSiteForm(Form):
    base_url = fields.TextField(validators=[validators.required()])