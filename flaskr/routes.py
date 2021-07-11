import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from pymodbus.exceptions import ConnectionException
from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import app, db, bcrypt
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        special = bool(form.user_type.data == "Especial")
        user = Users(
            name=form.name.data,
            reg_number=form.reg_number.data,
            email=form.email.data,
            password=hashed_password,
            special=special,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Conta criada para {form.name.data}.", "success")
    print("Erros no formulário de cadastro: {}".format(form.errors))

    return render_template("register.html", title="Cadastro", form=form)


@app.route("/log")
def log():
    """Rota - Histórico"""

    users = Users.query.all()

    return render_template("log.html", title="Histórico", data=users)


@app.route("/forgot")
def forgot():
    """Rota - Esqueceu a senha"""

    form = ForgotForm()
    return render_template("forgot.html", title="Esqueceu a senha?", form=form)


@app.route("/logout")
def logout():
    """Rota - Logout"""

    logout_user()
    return redirect(url_for("login"))
