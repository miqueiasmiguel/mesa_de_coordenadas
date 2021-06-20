import sqlite3

connection = sqlite3.connect(
    "C:/Users/mique/Documents/github/Mesa de Coordenadas/database/storage.db"
)

cursor = connection.cursor()

# Parametros da tabela users
REG_NUMBER = 11428214
NAME = "Miquéias Miguel da Silva Filho"
EMAIL = "miqueias.filho@cear.ufpb.br"
PASSWORD = "senhadificil"
SPECIAL = False

# Parametros da tabela positions
X_AXIS = 1
Y_AXIS = 1
DATE_TIME = "06-14-2021 10:31:12"
TRAJECTORY = None
USER_REG = 11428214

# Parametros da tabela sessions
DATE = "06-14-2021"
LOGIN_TIME = "10:20:15"
LOGOUT_TIME = "10:35:45"
USER_REG = 11428214

cursor.execute(
    """
INSERT INT  O users (reg_number, name, email, password, special)
VALUES (?, ?, ?, ?, ?)
""",
    (REG_NUMBER, NAME, EMAIL, PASSWORD, SPECIAL),
)


cursor.execute(
    """
INSERT INTO positions (x_axis, y_axis, date_time, trajectory, user_reg)
VALUES (?, ?, ?, ?)
""",
    (X_AXIS, Y_AXIS, DATE_TIME, TRAJECTORY, USER_REG),
)

cursor.exeute(
    """
INSERT INTO sessions (date, login_time, logout_time, user_reg)
VALUES (?, ?, ?, ?)
""",
    (DATE, LOGIN_TIME, LOGOUT_TIME, USER_REG),
)

cursor.execute(
    """
SELECT name FROM users WHERE reg_number = ?
""",
    (REG_NUMBER),
)

cursor.execute(
    """
DELETE FROM users WHERE reg_number = ?
""",
    (REG_NUMBER),
)

cursor.execute(
    """
    SELECT u.name, p.x_axis, p.y_axis, p.date_time
    FROM users AS u, positions AS p
    WHERE u.id = p.user_id
    ORDER BY name ASC
"""
)
