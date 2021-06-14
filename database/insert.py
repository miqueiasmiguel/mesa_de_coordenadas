import sqlite3

connection = sqlite3.connect("banco.db")

cursor = connection.cursor()

# Parametros da tabela users
ID = 1
NAME = "Miquéias"
REGISTRATION_NUMBER = 11428214
EMAIL = "miqueias.filho@cear.ufpb.br"
PASSWORD = "senhadificil"
SPECIAL = False

# Parametros da tabela positions
X_AXIS = 1
Y_AXIS = 1
DATE_TIME = "06-14-2021 10:31:12"
USER_ID = 1

# Parametros da tabela sessions
DATE = "06-14-2021"
LOGIN_TIME = "10:20:15"
LOGOUT_TIME = "10:35:45"
USER_ID = 1

cursor.execute(
    """
INSERT INTO users (id, name, registration_number, email, password, special)
VALUES (?, ?, ?, ?, ?)
""",
    (ID, NAME, REGISTRATION_NUMBER, EMAIL, PASSWORD, SPECIAL),
)

cursor.execute(
    """
INSERT INTO positions (x_axis, y_axis, date_time, user_id)
VALUES (?, ?, ?, ?)
""",
    (X_AXIS, Y_AXIS, DATE_TIME, USER_ID),
)

cursor.exeute(
    """
INSERT INTO sessions (date, login_time, logout_time, user_id)
VALUES (?, ?, ?, ?)
""",
    (DATE, LOGIN_TIME, LOGOUT_TIME, USER_ID),
)

cursor.execute(
    """
SELECT name FROM users WHERE id = ?
""",
    (ID),
)

cursor.execute(
    """
DELETE FROM users WHERE id = ?
""",
    (ID),
)
