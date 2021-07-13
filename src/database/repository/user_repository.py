import sqlite3
from typing import List, Tuple


class UserRepository:
    """Classe para administrar o repositório de 'users'"""

    def insert_user(
        self, reg_number: int, name: str, email: str, password: str, special: bool
    ) -> Tuple:
        """Insere um novo usuário na tabela 'users'
        :param reg_number: Matrícula do usuário
        :param name: Nome do usuário
        :param email: E-mail do usuário
        :param password: Senha da conta
        :param special: Indica se o usuário possui privilégios
        :return: Tupla com o novo usuário inserido
        """

        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        INSERT INTO users (reg_number, name, email, password, special)
        VALUES (?, ?, ?, ?, ?)
        """,
            (reg_number, name, email, password, special),
        )
        connection.commit()
        connection.close()

        return (reg_number, name, email, password, special)

    def select_all(self) -> List[Tuple]:
        """Consulta todos  os usuários na tabela 'usuário'
           com os atributos: matrícula, nome, e-mail e
           especial

        :return: Lista contendo tuplas com as informações
                 dos usuários
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT reg_number, name, email, special
        FROM users
        """
        )
        rows = cursor.fetchall()

        return rows
