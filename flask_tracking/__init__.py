from flask import Flask

from .data import db
from .tracking.views import tracking

app = Flask(__name__)
app.config.from_object('config')


@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 2}}

db.init_app(app)

app.register_blueprint(tracking)
