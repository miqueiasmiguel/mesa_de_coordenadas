from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "26bea9fc38afd17bd034bf4234e4f6fb"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from flaskr import routes
