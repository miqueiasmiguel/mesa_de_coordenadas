from datetime import datetime
from flaskr import db  # pylint: disable=no-member


class Users(db.Model):
    """Entidade Users"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    registration_number = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    positions = db.relationship("Positions")

    def __repr__(self):
        return f"User('{self.name}', '{self.registration_number}', '{self.email}')"


class Positions(db.Model):
    """Entidade Positions"""

    id = db.Column(db.Integer, primary_key=True)
    x_axis = db.Column(db.Integer)
    y_axis = db.Column(db.Integer)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"Position('{self.x_axis}', '{self.y_axis}', '{self.date_time}')"
