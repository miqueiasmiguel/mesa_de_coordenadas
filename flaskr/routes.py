import os
import io
import smtplib
import csv
from email.message import EmailMessage
from os.path import join, dirname, realpath
import sqlite3
from werkzeug.utils import secure_filename
from pymodbus.exceptions import ConnectionException
from flask import render_template, flash, url_for, redirect, request, Response
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import app, db
from src.serial_modules import configure_client, move_by_point, move_by_trajectory
from .forms import (
    ConfigurePort,
    RegistrationForm,
    LoginForm,
    ForgotForm,
    ControlTableForm,
)
from .models import Users


def allowed_file(filename):
    """Define se o arquivo possui uma extensão válida
    :param filename: recebe o nome do arquivo
    :return: verdadeiro ou falso depenendo se é um
             um arquivo válido ou não
    """

    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    """Rota - Login"""

    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(reg_number=form.reg_number.data).first()
        if user:
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Rota - Principal"""

    user = current_user
    user_reg = user.reg_number

    configure_form = ConfigurePort()
    control_form = ControlTableForm()

    if configure_form.configure_submit.data and configure_form.validate_on_submit():
        global client
        port = configure_form.port.data
        baudrate = int(configure_form.baudrate.data)
        client = configure_client(port, baudrate)

    if control_form.control_submit.data and control_form.validate_on_submit():
        x_axis = control_form.x_axis.data
        y_axis = control_form.y_axis.data

        if x_axis == "":
            x_axis = 0
        if y_axis == "":
            y_axis = 0
        if x_axis != 0:
            x_axis = int(control_form.x_axis.data)
        if y_axis != 0:
            y_axis = int(control_form.y_axis.data)

        move_type = request.form["move_type"]

        if control_form.trajectory:
            print("Existe uma trajetória!")
            file = request.files["trajectory"]
            if file.filename == "":
                print("No filename")
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                print("File '{}' saved!".format(filename))

        print("X: {} e seu tipo é {}".format(x_axis, type(x_axis)))
        print("Y: {} e seu tipo é {}".format(y_axis, type(y_axis)))
        print("Tipo de movimento: {}".format(move_type))

        if move_type == 0:
            try:
                move_by_point(
                    x_axis=x_axis, y_axis=y_axis, user_reg=user_reg, client=client
                )
            except ConnectionException:
                flash("Erro ao tentar conectar", "error")

        if move_type == 1:
            try:
                move_by_trajectory(
                    path=join(join(dirname(realpath(__file__)), "files"), filename),
                    client=client,
                    user_reg=user_reg,
                )
            except Exception:
                flash("Ocorreu algum erro", "error")

    print("Erros no formulário de controle: {}".format(control_form.errors))
    print("Erros no formulário de movimento: {}".format(configure_form.errors))

    return render_template(
        "home.html", title="home", configure_form=configure_form, move_form=control_form
    )


@app.route("/register", methods=["GET", "POST"])
# @login_required
def register():
    """Rota - Register"""

    form = RegistrationForm()
    if form.validate_on_submit():
        special = bool(form.user_type.data == "Especial")
        user = Users(
            name=form.name.data,
            reg_number=form.reg_number.data,
            email=form.email.data,
            password=form.password.data,
            special=special,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Conta criada para {form.name.data}.", "success")
    print("Erros no formulário de cadastro: {}".format(form.errors))

    return render_template("register.html", title="Cadastro", form=form)


@app.route("/position_log")
def position_log():
    """Rota - Histórico de posições"""

    connection = sqlite3.connect("flaskr/storage.db")
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT u.name, p.x_axis, p.y_axis, p.trajectory, p.date_time
    FROM users AS u, positions AS p
    WHERE u.id = p.user_id
    """
    )
    positions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "position_log.html",
        title="Histórico de posições",
        positions=positions,
    )


@app.route("/session_log")
def session_log():
    """Rota - Histórico de sessões"""

    connection = sqlite3.connect("flaskr/storage.db")
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT u.reg_number, u.name, s.login_time, ((JULIANDAY(s.logout_time) - JULIANDAY(s.login_time))*24*60) AS periodo
    FROM users u, sessions s
    WHERE u.id  =  s.user_id
    ORDER BY s.login_time DESC
    """
    )
    sessions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "session_log.html",
        title="Histórico de sessões",
        sessions=sessions,
    )


@app.route("/registered_users")
def registered_users():
    """Rota - Usuários cadastrados"""

    connection = sqlite3.connect("flaskr/storage.db")
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT reg_number, name, email, special
    FROM users
    """
    )
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "registered_users.html", title="Usuários cadastrados", users=users
    )


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Rota - Esqueceu a senha"""

    form = ForgotForm()

    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            print("Existe um usuáro com este e-mail")
            server = smtplib.SMTP(host="smtp.gmail.com", port=587)
            server.starttls()
            server.login("mesacoordenadasufpb@gmail.com", "informaticaindustrialalunos")

            msg = EmailMessage()
            msg.set_content(user.password)

            msg["Subject"] = "Senha da mesa de coordenadas"
            msg["From"] = "mesacoordenadasufpb@gmail.com"
            msg["To"] = f"{user.email}"

            server.send_message(msg)
            server.quit()

            flash(f"Senha enviada para {form.email.data}", "success")
        if not user:
            flash(
                f"Não existe um usuário cadastrado com o e-mail {form.email.data}",
                "error",
            )
    return render_template("forgot.html", title="Esqueceu a senha?", form=form)


@app.route("/download/position_log")
def download_position():
    """Rota - Download da posição"""

    connection = sqlite3.connect("flaskr/storage.db")
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT u.name, p.x_axis, p.y_axis, p.trajectory, p.date_time
    FROM users AS u, positions AS p
    WHERE u.id = p.user_id
    """
    )
    positions = cursor.fetchall()

    cursor.close()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ["Nome", "Eixo X", "Eixo Y", "Trajetoria", "Data e hora"]
    writer.writerow(line)
    line = []
    for position in positions:
        line = [
            position[0]
            + ","
            + str(position[1])
            + ","
            + str(position[2])
            + ","
            + str(position[3])
            + ","
            + str(position[4])
        ]
        writer.writerow(line)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=historico_de_posicoes.csv"
        },
    )


@app.route("/download/session_log")
def download_session():
    """Rota - Download da posição"""

    connection = sqlite3.connect("flaskr/storage.db")
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT u.reg_number, u.name, s.login_time, ((JULIANDAY(s.logout_time) - JULIANDAY(s.login_time))*24*60) AS periodo
    FROM users u, sessions s
    WHERE u.id  =  s.user_id
    ORDER BY s.login_time DESC
    """
    )
    sessions = cursor.fetchall()

    cursor.close()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ["Matrícula", "Nome", "Hora do login", "Duração"]
    writer.writerow(line)
    line = []
    for session in sessions:
        line = [
            str(session[0])
            + ","
            + str(session[1])
            + ","
            + str(session[2])
            + ","
            + str(session[3])
        ]
        writer.writerow(line)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=historico_de_sessoes.csv"},
    )


@app.route("/download/users")
def download_users():
    """Rota - Download da posição"""

    connection = sqlite3.connect("flaskr/storage.db")
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT reg_number, name, email, special
    FROM users
    """
    )
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ["Matrícula", "Nome", "E-mail", "Especial"]
    writer.writerow(line)
    line = []
    for user in users:
        line = [str(user[0]) + "," + user[1] + "," + user[2] + "," + str(user[3])]
        writer.writerow(line)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=lista_de_usuarios.csv"},
    )


@app.route("/logout")
def logout():
    """Rota - Logout"""

    logout_user()
    return redirect(url_for("login"))
