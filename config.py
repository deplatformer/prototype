import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))
USER_DATA_DIR = "_user_data/"

# Flask settings
SECRET_KEY = '3d488586-35ec-4706-ab35-cb46e59f11b6'

# Powergate address
POWERGATE_ADDRESS = "127.0.0.1:5002"

# Flask-SQLAlchemy settings
# File-based SQL database
SQLALCHEMY_DATABASE_URI = 'sqlite:///deplatformr.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

# Flask-User settings
# See https://flask-user.readthedocs.io/en/latest/configuring_settings.html
# Shown in and email templates and page footers
USER_APP_NAME = "Deplatformr - Prototype"
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_CONFIRM_EMAIL = False
USER_REQUIRE_RETYPE_PASSWORD = True
USER_ENABLE_CHANGE_USERNAME = False
USER_ENABLE_CHANGE_PASSWORD = True
USER_ENABLE_REMEMBER_ME = False
USER_AUTO_LOGIN = True
USER_AUTO_LOGIN_AFTER_CONFIRM = True
USER_AUTO_LOGIN_AFTER_REGISTER = True
USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = True
USER_AUTO_LOGIN_AT_LOGIN = True
USER_AFTER_LOGOUT_ENDPOINT = "user.login"
