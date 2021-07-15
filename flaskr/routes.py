from datetime import datetime
import os
import json
from time import time
from os.path import join, dirname, realpath
from pymodbus.exceptions import ConnectionException
from pymodbus.client.sync import ModbusSerialClient as RTUClient
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
from src import ControlTable, CSVWriter, SendEmail, LoginTime
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

login_time = LoginTime()
control = ControlTable()
client = RTUClient(
    method="rtu", port="COM4", baudrate=115200, parity="N", timeout=1, bytesize=8
)


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
            login_time.set_login()
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash("Matrícula ou senha incorretos.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Rota - Principal"""

    repository = PositionRepository()

    configure_form = ConfigurePort()
    control_form = ControlTableForm()

    if configure_form.configure_submit.data and configure_form.validate_on_submit():
        client.port = configure_form.port.data
        client.baudrate = int(configure_form.baudrate.data)

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
                response = control.move_by_point(
                    def_x=x_axis,
                    def_y=y_axis,
                    x_speed=x_speed,
                    y_speed=y_speed,
                    client=client,
                )

                repository.insert_position(
                    x_axis=response["act_x"],
                    y_axis=response["act_y"],
                    date_time=datetime.now(),
                    x_speed=response["x_speed"],
                    y_speed=response["y_speed"],
                    user_id=current_user.id,
                )
            except NameError:
                flash("Por favor, configure a porta serial.", "error")
            except ConnectionException:
                flash("Erro ao tentar conectar.", "error")

        if move_type == 1:
            try:
                with open(
                    join(join(dirname(realpath(__file__)), "files"), filename), "r"
                ) as file:
                    for linha in file:
                        pontos = linha.split()
                        x_axis = int(pontos[0])
                        y_axis = int(pontos[1])
                        
                        response = control.move_by_point(
                            def_x=x_axis,
                            def_y=y_axis,
                            x_speed=x_speed,
                            y_speed=y_speed,
                            client=client,
                        )
                        repository.insert_position(
                            x_axis=response["act_x"],
                            y_axis=response["act_y"],
                            date_time=datetime.now(),
                            x_speed=response["x_speed"],
                            y_speed=response["y_speed"],
                            user_id=current_user.id,
                            trajectory=filename,
                        )
                    file.close()
            except NameError:
                flash("Por favor, configure a porta serial.", "error")
            except ConnectionException:
                flash("Erro ao tentar conectar.", "error")

    return render_template(
        "home.html",
        title="home",
        configure_form=configure_form,
        move_form=control_form,
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

            send_email = SendEmail()
            send_email.send_email(user.email, user.password)

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

    csv_writer = CSVWriter()
    output = csv_writer.positions_csv(positions)

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

    csv_writer = CSVWriter()
    output = csv_writer.sessions_csv(sessions)

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

    csv_writer = CSVWriter()
    output = csv_writer.users_csv(users)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=lista_de_usuarios.csv"},
    )


@app.route("/logout")
def logout():
    """Rota - Logout"""

    repository = SessionRepository()
    repository.insert_session(
        login_time=login_time.get_login(),
        logout_time=datetime.now(),
        user_id=current_user.id,
    )
    logout_user()

    return redirect(url_for("login"))


@app.route("/data", methods=["GET", "POST"])
def data():
    """Dados da mesa de coordenadas"""

    dados = [time() * 1000, control.get_act_x(), control.get_act_y()]

    response = make_response(json.dumps(dados))
    response.content_type = "application/json"

    return response


@app.route("/help")
def help_page():
    """Rota - Ajuda"""

    return render_template("help.html", title="Ajuda")
