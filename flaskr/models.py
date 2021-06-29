from flask_login import UserMixin
from flaskr import db, login_manager


@login_manager.user_loader
def user_loader(reg_number):
    """
    Função que busca no banco de dados o
    usuário que será logado

    :returns: Usuário a ser logado
    """
    return Users.query.get(int(reg_number))


class Users(db.Model, UserMixin):
    """Entidade - Users"""

    __table__ = db.Model.metadata.tables["users"]

    def __repr__(self):
        return f"User('{self.name}', '{self.reg_number}', '{self.special}')"


class Positions(db.Model):
    """Entidade - Positions"""

    __table__ = db.Model.metadata.tables["positions"]

    def __repr__(self):
        return f"Position('{self.user_reg}', '{self.x_axis}', '{self.y_axis}', '{self.date_time}')"


class Sessions(db.Model):
    """Entidade - Sessions"""

    __table__ = db.Model.metadata.tables["sessions"]

    def __repr__(self):
        return f"Session('{self.user_reg}', '{self.date}', '{self.login_time}', '{self.logout_time}')"
