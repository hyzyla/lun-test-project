from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import view, models
from .model_views.group import *
from .model_views.building import *
from .model_views.flat import *
from .model_views.city import *