import sqlite3
from datetime import datetime
from typing import Tuple


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

    def delete_session(self, id: int):
        """Deleta uma sessão na tabela 'sessions'
        :param id: id da sessão
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        DELETE FROM sessions WHERE id = ?
        """,
            (id,),
        )
        connection.commit()
        connection.close()
