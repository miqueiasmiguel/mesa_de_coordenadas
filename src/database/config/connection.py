import sqlite3
from sqlite3.dbapi2 import Connection
from typing import Type
from sqlite3 import Error


def create_connection(db_file: str) -> Type[Connection]:
    """Cria um objeto de conexão para um banco de dados SQLite
    :param db_file: Caminho de conexão do banco. Se não houver
                nenhum banco nesse caminho, um novo será criado
    :return: Objeto de conexão ou None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)

    return conn
