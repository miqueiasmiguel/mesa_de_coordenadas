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

    def delete_user(self, reg_number):
        """Deleta um usuário na tabela 'users'
        :param reg_number: Matrícula do usuário
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        DELETE FROM users WHERE reg_number = ?
        """,
            (reg_number,),
        )
        connection.commit()
        connection.close()

    def select_user(self, reg_number: int) -> List[Tuple]:
        """Consulta um usuário na tabela 'usuário'
        :param user_reg: Matrícula do usuário
        :return: Lista contendo tuplas com as informações
                 dos usuários
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT * FROM users WHERE reg_number = ?
        """,
            (reg_number,),
        )
        rows = cursor.fetchall()

        return rows
