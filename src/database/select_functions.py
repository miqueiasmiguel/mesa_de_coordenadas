import sqlite3


connection = sqlite3.connect("storage.db")
cursor = connection.cursor()

# funcoes de ordenar por

atributo = ""
atributo_data = ""
asc_desc = ""
atributo_filtro = ""
filtro = ""
data1 = ""
data2 = ""

# tabela do historico com organizacao de ordem pelo atributo selecionado

cursor.execute(
    """
SELECT u.name, p.x_axis, p.y_axis, p.state, p.trajectory, p.velocity, p.date_time
FROM users AS u, positions AS p
WHERE u.reg_number = p.user_reg
ORDER BY ? ?
"""(
        atributo, asc_desc
    )
)

cursor.execute(
    """
SELECT u.reg_number, u.name, s.login_time, ((JULIANDAY(s.logout_time) - JULIANDAY(s.login_time))*24*60) AS periodo
FROM users u, sessions s
WHERE u.reg_number  =  s.user_reg
ORDER BY ? ?
"""(
        atributo, asc_desc
    )
)

# filtro do historico
cursor.execute(
    """
SELECT u.reg_number, u.name, s.login_time, ((JULIANDAY(s.logout_time) - JULIANDAY(s.login_time))*24*60) AS periodo
FROM users AS u, sessions AS s
WHERE u.reg_number  =  s.user_reg AND ? = ?
ORDER BY ? ?
"""(
        atributo_filtro, filtro, atributo, asc_desc
    )
)

cursor.execute(
    """
SELECT u.name, p.x_axis, p.y_axis, p.state, p.trajectory, p.velocity, p.date_time
FROM users AS u, positions AS p
WHERE u.reg_number = p.user_reg AND ? = ?
ORDER BY ? ?
"""(
        atributo_filtro, filtro, atributo, asc_desc
    )
)

# filtro de datas
cursor.execute(
    """
SELECT u.name, p.x_axis, p.y_axis, p.state, p.trajectory, p.velocity, p.date_time
FROM users AS u, positions AS p
WHERE u.reg_number = p.user_reg AND ? > ? AND ? < ?
ORDER BY ? ?
"""(
        atributo_data, data1, atributo_data, data2, atributo, asc_desc
    )
)

cursor.execute(
    """
SELECT u.reg_number, u.name, s.login_time, ((JULIANDAY(s.logout_time) - JULIANDAY(s.login_time))*24*60) AS periodo
FROM users AS u, sessions AS s
WHERE u.reg_number = p.user_reg AND ? > ? AND ? < ?
ORDER BY ? ?
"""(
        atributo_data, data1, atributo_data, data2, atributo, asc_desc
    )
)
