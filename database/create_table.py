import sqlite3

# Cria um objeto de conexão que representa o banco de dados
# Aqui, os dados serão armazenados em 'banco.db'
connection = sqlite3.connect("banco.db")

# Cria um objeto de cursor capaz de executar comandos SQL
cursor = connection.cursor()

# Executa comandos SQL
cursor.execute(
    """
CREATE TABLE users(
    id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    registration_number INTEGER NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    special BOOLEAN NOT NULL,
    PRIMARY KEY(id ASC)
)
"""
)

cursor.execute(
    """
CREATE TABLE positions(
    id INTEGER NOT NULL,
    x_axis INTEGER NOT NULL,
    y_axis INTEGER NOT NULL,
    date_time DATETIME NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id ASC),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
"""
)

cursor.execute(
    """
CREATE TABLE sessions(
    id INTEGER NOT NULL,
    date DATE NOT NULL,
    login_time TIME NOT NULL,
    logout_time TIME NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY(id ASC),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
"""
)
