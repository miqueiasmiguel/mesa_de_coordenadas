from datetime import datetime
from flask_login import UserMixin
from flaskr import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    """
    Função que busca no banco de dados o
    usuário que será logado

    :returns: Usuário a ser logado
    """
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    """Entidade - Users"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    registration_number = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    special = db.Column(db.Boolean, nullable=False)
    positions = db.relationship("Positions")

    def __repr__(self):
        return f"User('{self.name}', '{self.registration_number}', '{self.email}')"


class Positions(db.Model):
    """Entidade - Positions"""

    id = db.Column(db.Integer, primary_key=True)
    x_axis = db.Column(db.Integer, nullable=False)
    y_axis = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"Position('{self.x_axis}', '{self.y_axis}', '{self.date_time}')"
