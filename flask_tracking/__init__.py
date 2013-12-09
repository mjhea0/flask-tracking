from flask import Flask

from .auth import login_manager
from .data import db
import flask_tracking.errors as errors
import flask_tracking.logs as logs
from .tracking.views import tracking
from .users.views import users

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')


@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 3}}

# Setup extensions
db.init_app(app)
login_manager.init_app(app)

# Internal extensions for managing
# logs and adding error handlers
logs.init_app(app, remove_existing_handlers=True)
errors.init_app(app)

app.register_blueprint(tracking)
app.register_blueprint(users)
