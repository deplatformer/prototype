from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

app = Flask(__name__, static_folder="static")
app.config.from_object("config")
db = SQLAlchemy(app)

# These imports need to come after the app is instantiated
from deplatformr.views import views, facebook_views, filecoin_views
from deplatformr.models import user_models, filecoin_models

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, user_models.User)
