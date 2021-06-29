"""
Rode este script para criar um banco de dados
SQLite com as tabelas aqui definidas
"""

from src.database.config import create_connection

# Substitua a uri pelo caminho desejado
# Aqui, os dados serão armazenados em 'storage.db'
connection = create_connection("flaskr/storage.db")

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_number INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        special BOOLEAN NOT NULL
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        x_axis INTEGER NOT NULL,
        y_axis INTEGER NOT NULL,
        date_time DATETIME NOT NULL,
        trajectory BLOB,
        state VARCHAR NOT NULL,
        velocity REAL NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login_time DATETIME NOT NULL,
        logout_time DATETIME NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
"""
)
