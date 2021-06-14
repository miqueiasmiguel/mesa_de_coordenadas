import sqlite3

connection = sqlite3.connect("banco.db")

cursor = connection.cursor()

# funcoes de ordenar por
# tabela do historico com os pontos da mesa
cursor.execute(
    """
    SELECT u.name, p.x_axis, p.y_axis, p.date_time
    FROM users AS u, positions AS p
    WHERE u.id = p.user_id
    ORDER BY name ASC
"""
)
