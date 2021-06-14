import sqlite3

connection = sqlite3.connect("banco.db")

cursor = connection.cursor()

cursor.execute(
    """
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition
"""
)
