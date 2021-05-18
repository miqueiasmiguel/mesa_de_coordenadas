from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "26bea9fc38afd17bd034bf4234e4f6fb"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
db = SQLAlchemy(app)

from flaskr import routes
