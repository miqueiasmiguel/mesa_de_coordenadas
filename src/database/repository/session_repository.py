import sqlite3
from datetime import datetime
from typing import Tuple, List


class SessionRepository:
    """Classe para administrar o repositório de 'sessions'"""

    def insert_session(
        self, login_time: datetime, logout_time: datetime, user_id: int
    ) -> Tuple:
        """Insere um novo registro de sessão na tabela 'sessions'
        :param login_time: Horário em que a sessão foi estabelecida
        :param logout_time: Horário em que a sessão foi finalizada
        :param user_id: Id do usuário que estabeleceu a sessão
        :return: Tupla com os dados da sessão
        """

        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        INSERT INTO sessions (login_time, logout_time, user_id)
        VALUES (?, ?, ?)
        """,
            (login_time, logout_time, user_id),
        )
        connection.commit()
        id = cursor.lastrowid
        connection.close()

        return (id, login_time, logout_time, user_id)

    def select_all(self) -> List[Tuple]:
        """Consulta todas  as sessões na tabela 'sessions'
           com os atributos: matrícula, nome, hora de login
           e a duração da sessão em minutos, ordenadas pela
           hora de login.

        :return: Lista contendo tuplas com as informações
                 das sessões
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT u.reg_number, u.name, s.login_time, ((JULIANDAY(s.logout_time) - JULIANDAY(s.login_time))*24*60)
        AS periodo
        FROM users u, sessions s
        WHERE u.id  =  s.user_id
        ORDER BY s.login_time DESC
        """
        )
        rows = cursor.fetchall()

        return rows
