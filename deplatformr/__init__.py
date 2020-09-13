from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

app = Flask(__name__, static_folder="static")
app.config.from_object("config")
db = SQLAlchemy(app)

from deplatformr import views, models

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, models.User)
