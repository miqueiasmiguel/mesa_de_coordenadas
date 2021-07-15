from functools import wraps
from flask_login import UserMixin, current_user
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


def requires_roles(*roles):
    """Função para definir que é necessário ser um
    usuário especial para acessar a página
    """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.special not in roles:
                # Redirect the user to an unauthorized notice!
                return "You are not authorized to access this page"
            return f(*args, **kwargs)

        return wrapped

    return wrapper
