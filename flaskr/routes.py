from datetime import datetime
import os
import io
import smtplib
import csv
import json
import struct
from time import time, sleep
from email.message import EmailMessage
from os.path import join, dirname, realpath
from pymodbus.exceptions import ConnectionException
from werkzeug.utils import secure_filename
from flask import (
    render_template,
    flash,
    url_for,
    redirect,
    request,
    Response,
    make_response,
)
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import app, db
from src.serial_modules import configure_client
from src.database.repository import (
    SessionRepository,
    PositionRepository,
    UserRepository,
)
from .forms import (
    ConfigurePort,
    RegistrationForm,
    LoginForm,
    ForgotForm,
    ControlTableForm,
)
from .models import Users, requires_roles


login_time = 0
logout_time = 0
act_x = 0
act_y = 0


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
            global login_time
            login_time = datetime.now()
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Rota - Principal"""

    user = current_user

    repository = PositionRepository()

    configure_form = ConfigurePort()
    control_form = ControlTableForm()

    global act_x
    global act_y

    if configure_form.configure_submit.data and configure_form.validate_on_submit():
        port = configure_form.port.data
        baudrate = int(configure_form.baudrate.data)
        global client
        client = configure_client(port, baudrate)

    if control_form.control_submit.data and control_form.validate_on_submit():

        x_axis = control_form.x_axis.data
        y_axis = control_form.y_axis.data

        if x_axis == "":
            x_axis = 0
        if y_axis == "":
            y_axis = 0
        if x_axis != 0:
            try:
                x_axis = int(control_form.x_axis.data)
            except ValueError:
                flash("Por favor, digite valores inteiros no eixo X.", "error")
        if y_axis != 0:
            try:
                y_axis = int(control_form.y_axis.data)
            except ValueError:
                flash("Por favor, digite valores inteiros no eixo Y.", "error")

        x_speed = control_form.x_speed.data
        y_speed = control_form.y_speed.data
        print("Velocidade X: {}\nSeu tipo: {}".format(x_speed, type(x_speed)))
        print("Velocidade Y: {}\nSeu tipo: {}".format(y_speed, type(y_speed)))

        if x_speed != 0:
            try:
                x_speed = int(control_form.x_speed.data)
            except ValueError:
                flash(
                    "Por favor, digite valores inteiros para a velocidade no eixo X.",
                    "error",
                )
        if y_speed != 0:
            try:
                y_speed = int(control_form.y_speed.data)
            except ValueError:
                flash(
                    "Por favor, digite valores inteiros para a velocidade no eixo Y.",
                    "error",
                )

        try:
            client.connect()
            sleep(1.7)
            client.write_register(544, x_speed, unit=1)
            client.write_register(560, x_speed, unit=1)
        except ConnectionException:
            flash("Erro ao tentar conectar-se", "error")
        except struct.error:
            flash(
                "Você não definiu uma velocidade ou o valor definido não é um inteiro"
            )

        move_type = int(request.form["move_type"])

        if control_form.trajectory:
            file = request.files["trajectory"]
            if file.filename == "":
                print("No filename")
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                print("File '{}' saved!".format(filename))

        if move_type == 0:
            try:
                client.connect()
                sleep(1.7)
                client.write_register(512, x_axis, unit=1)
                timeout = time() + 7
                while True:
                    x_response = client.read_holding_registers(220, 1, unit=1)
                    act_x = x_response.registers[0]
                    print("X: {}".format(act_x))
                    if time() > timeout:
                        print("Erro de Timeout")
                        break
                    if x_axis == act_x:
                        print("Eixo X OK!")
                        break

                client.write_register(528, y_axis, unit=1)
                timeout = time() + 7
                while True:
                    y_response = client.read_holding_registers(230, 1, unit=1)
                    act_y = y_response.registers[0]
                    print("Y: {}".format(act_y))
                    if time() > timeout:
                        print("Erro de timeout")
                        break
                    if y_axis == act_y:
                        print("Eixo Y OK!")
                        break

                repository.insert_position(
                    x_axis=act_x,
                    y_axis=act_x,
                    date_time=datetime.now(),
                    user_id=user.id,
                )
            except NameError:
                flash("Por favor, configure a porta serial.", "error")
            except ConnectionException:
                flash("Erro ao tentar conectar-se.", "error")

        if move_type == 1:
            try:
                with open(
                    join(join(dirname(realpath(__file__)), "files"), filename), "r"
                ) as file:
                    for linha in file:
                        pontos = linha.split()
                        x_axis = int(pontos[0])
                        y_axis = int(pontos[1])
                        client.connect()
                        sleep(1.7)
                        client.write_register(512, x_axis, unit=1)
                        timeout = time() + 7
                        while True:
                            x_response = client.read_holding_registers(220, 1, unit=1)
                            act_x = x_response.registers[0]
                            print("X: {}".format(act_x))
                            if time() > timeout:
                                print("Erro de Timeout")
                                break
                            if x_axis == act_x:
                                print("Eixo X OK!")
                                break

                        client.write_register(528, y_axis, unit=1)
                        timeout = time() + 7
                        while True:
                            y_response = client.read_holding_registers(230, 1, unit=1)
                            act_y = y_response.registers[0]
                            print("Y: {}".format(act_y))
                            if time() > timeout:
                                print("Erro de timeout")
                                break
                            if y_axis == act_y:
                                print("Eixo Y OK!")
                                break

                        repository.insert_position(
                            x_axis=act_x,
                            y_axis=act_x,
                            date_time=datetime.now(),
                            user_id=user.id,
                            trajectory=filename,
                        )
                    file.close()
            except Exception:
                flash("Ocorreu algum erro", "error")

    return render_template(
        "home.html",
        title="home",
        configure_form=configure_form,
        move_form=control_form,
        act_x=act_x,
        act_y=act_y,
    )


@app.route("/register", methods=["GET", "POST"])
@login_required
@requires_roles(True)
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
@login_required
@requires_roles(True)
def position_log():
    """Rota - Histórico de posições"""

    repository = PositionRepository()
    positions = repository.select_all()

    return render_template(
        "position_log.html",
        title="Histórico de posições",
        positions=positions,
    )


@app.route("/session_log")
@login_required
@requires_roles(True)
def session_log():
    """Rota - Histórico de sessões"""

    repository = SessionRepository()
    sessions = repository.select_all()

    return render_template(
        "session_log.html",
        title="Histórico de sessões",
        sessions=sessions,
    )


@app.route("/registered_users")
@login_required
@requires_roles(True)
def registered_users():
    """Rota - Usuários cadastrados"""

    repository = UserRepository()
    users = repository.select_all()

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
@login_required
@requires_roles(True)
def download_position():
    """Rota - Download da posição"""

    repository = PositionRepository()
    positions = repository.select_all()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ["Nome", "Eixo X", "Eixo Y", "Trajetoria", "Data e hora"]
    writer.writerow(line)
    for position in positions:
        line = []
        line.append(position[0])
        line.append(position[1])
        line.append(position[2])
        line.append(position[3])
        line.append(position[4])
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
@login_required
@requires_roles(True)
def download_session():
    """Rota - Download da posição"""

    repository = SessionRepository()
    sessions = repository.select_all()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ["Matrícula", "Nome", "Hora do login", "Duração (min)"]
    writer.writerow(line)

    for session in sessions:
        line = []
        line.append(session[0])
        line.append(session[1])
        line.append(session[2])
        line.append(session[3])
        writer.writerow(line)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=historico_de_sessoes.csv"},
    )


@app.route("/download/users")
@login_required
@requires_roles(True)
def download_users():
    """Rota - Download da posição"""

    repository = UserRepository()
    users = repository.select_all()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ["Matrícula", "Nome", "E-mail", "Especial"]
    writer.writerow(line)
    for user in users:
        line = []
        line.append(user[0])
        line.append(user[1])
        line.append(user[2])
        line.append(user[3])
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

    logout_time = datetime.now()
    user = current_user
    repository = SessionRepository()

    repository.insert_session(
        login_time=login_time, logout_time=logout_time, user_id=user.id
    )

    logout_user()

    return redirect(url_for("login"))


@app.route("/data", methods=["GET", "POST"])
def data():
    """Dados da mesa de coordenadas"""

    global act_x
    global act_y

    data = [time() * 1000, act_x, act_y]

    response = make_response(json.dumps(data))
    response.content_type = "application/json"

    return response


@app.route("/help")
def help():
    """Rota - Ajuda"""

    return render_template("help.html", title="Ajuda")
