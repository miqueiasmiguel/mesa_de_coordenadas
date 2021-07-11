import sqlite3
import datetime
from typing import Any, Tuple


class PositionRepository:
    """Classe para administrar o repositório de 'positions'"""

    def insert_position(
        self,
        x_axis: int,
        y_axis: int,
        date_time: datetime,
        trajectory: Any,
        user_reg: int,
    ) -> Tuple:
        """Insere uma nova posição na tabela 'positions'
        :param x_axis: Posição no eixo x
        :param y_axis: Posição no eixo y
        :param date_time: Data e hora do registro
        :param trajectory: Arquivo de trajetória
        :param user_reg: Matrícula do usuário que está
                         definindo a posição
        :return: Tupla com uma nova posição inserida
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        INSERT INTO positions (x_axis, y_axis, date_time, trajectory, user_reg)
        VALUES (?, ?, ?, ?, ?)
        """,
            (x_axis, y_axis, date_time, trajectory, user_reg),
        )
        connection.commit()
        id = cursor.lastrowid
        connection.close()

        return (id, x_axis, y_axis, date_time, trajectory, user_reg)

    def delete_position(self, id: int):
        """Deleta uma posição na tabela 'positions'
        :param id: id da posição
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        DELETE FROM positions WHERE id = ?
        """,
            (id,),
        )
        connection.commit()
        connection.close()
