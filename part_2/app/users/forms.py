from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, RecaptchaField, fields, validators
from flask.ext.wtf import Required, Email, EqualTo
from app.users.models import User
from app import db

class LoginForm(Form):
    name = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        print self.name.data, "here"
        return db.session.query(User).filter_by(name=self.name.data).first()

class RegistrationForm(Form):
    name = fields.TextField(validators=[validators.required()])
    email = fields.TextField(validators=[validators.Email()])
    password = fields.PasswordField(validators=[validators.required()])
    conf_password = fields.PasswordField(validators=[validators.required()])
    def validate_login(self, field):
        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Duplicate username')