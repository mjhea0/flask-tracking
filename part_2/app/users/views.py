from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm, RegistrationForm
from app.users.models import User

mod = Blueprint('users', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@mod.route('/login/', methods=('GET', 'POST'))
def login_view():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template('users/login.html', form=form)

@mod.route('/register/', methods=('GET', 'POST'))
def register_view():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('users/register.html', form=form)

@login_required
@mod.route('/logout/')
def logout_view():
    logout_user()
    return redirect(url_for('index'))