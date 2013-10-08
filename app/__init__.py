from flask import Flask, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from flask.ext.login import LoginManager
import os

app = Flask(__name__) #create our application object
app.config.from_object('config.DebugConfiguration') #load our local config file

heroku = Heroku(app) #create a heroku config object from our app object

login_manager = LoginManager(app) #create a LoginManager Object from our app object

db = SQLAlchemy(app) #create a db (SQLAlchemy) object from our app object

#register the users module blueprint
from app.users.views import mod as usersModule
app.register_blueprint(usersModule)

#add our view as the login view to finish configuring the LoginManager
login_manager.login_view = "users.login_view"

#register the tracking module blueprint
from app.tracking.views import mod as trackingModule
app.register_blueprint(trackingModule)

#----------------------------------------
# controllers
#----------------------------------------

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def key_error(e):
    return render_template('400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('generic.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('generic.html'), 500


@app.route("/")
def index():
    return render_template('index.html')