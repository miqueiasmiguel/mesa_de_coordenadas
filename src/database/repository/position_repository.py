import sqlite3
from datetime import datetime
from typing import Tuple, List


class PositionRepository:
    """Classe para administrar o repositório de 'positions'"""

    def insert_position(
        self,
        x_axis: int,
        y_axis: int,
        date_time: datetime,
        user_id: int,
        x_speed: int,
        y_speed: int,
        trajectory=None,
    ) -> Tuple:
        """Insere uma nova posição na tabela 'positions'
        :param x_axis: Posição no eixo x
        :param y_axis: Posição no eixo y
        :param date_time: Data e hora do registro
        :param trajectory: Arquivo de trajetória
        :param user_id: id do usuário que está
                        definindo a posição
        :return: Tupla com uma nova posição inserida
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        INSERT INTO positions (x_axis, y_axis, date_time, trajectory, x_speed, y_speed, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (x_axis, y_axis, date_time, trajectory, x_speed, y_speed, user_id),
        )
        connection.commit()
        id = cursor.lastrowid
        connection.close()

        return (id, x_axis, y_axis, date_time, trajectory, user_id)

    def select_all(self) -> List[Tuple]:
        """Consulta todas  as posições na tabela 'positions'
            com os atributos: nome, eixo x, eixo y, trajetória
            e date e hora, ordenadas pelo horário em que a
            posição foi definida

        :return: Lista contendo tuplas com as informações
                 das posições
        """
        connection = sqlite3.connect("flaskr/storage.db")
        cursor = connection.cursor()
        cursor.execute(
            """
        SELECT u.name, p.x_axis, p.y_axis, p.trajectory, p.x_speed, p.y_speed, p.date_time
        FROM users AS u, positions AS p
        WHERE u.id = p.user_id
        ORDER BY p.date_time DESC
        """
        )
        rows = cursor.fetchall()

        return rows
