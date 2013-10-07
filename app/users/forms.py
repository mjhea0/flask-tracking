from flask.ext.wtf import Form, fields, validators
from flask.ext.wtf import Required, Email
from app.users.models import User
from app import db


def validate_login(form, field):
    user = form.get_user()

    if user is None:
        raise validators.ValidationError('Invalid user')

    if user.password != form.password.data:
        raise validators.ValidationError('Invalid password')


class LoginForm(Form):
    name = fields.TextField(validators=[Required()])
    password = fields.PasswordField(validators=[Required(), validate_login])

    def get_user(self):
        return db.session.query(User).filter_by(name=self.name.data).first()


class RegistrationForm(Form):
    name = fields.TextField(validators=[Required()])
    email = fields.TextField(validators=[Email()])
    password = fields.PasswordField(validators=[Required()])
    conf_password = fields.PasswordField(validators=[Required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Duplicate username')
