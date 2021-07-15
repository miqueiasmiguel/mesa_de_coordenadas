from datetime import datetime


class LoginTime:
    """Classe para administrar o tempo de login e logout"""

    def __init__(self):
        self.login_time = 0
        self.logout_time = 0

    def set_login(self):
        """Grava o instante em que ocorreu um login"""

        self.login_time = datetime.now()

    def set_logout(self):
        """Grava o instante em que ocorreu um logout"""

        self.logout_time = datetime.now()

    def get_login(self):
        """Retorna o instante em que ocorreu o login

        :return: horário de login
        """

        return self.login_time

    def get_logout(self):
        """Retorna o instante em que ocorreu o logout

        :return: horário de logout
        """

        return self.logout_time
