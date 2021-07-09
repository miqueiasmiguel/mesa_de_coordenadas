import json
from random import random
from time import time
from pymodbus.exceptions import ConnectionException
from flask import render_template, flash, url_for, redirect, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import app, db, bcrypt
from src.serial_modules import configure_client, move_by_point
from .forms import (
    ConfigurePort,
    RegistrationForm,
    LoginForm,
    ForgotForm,
    ControlTableForm,
)
from .models import Users


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

    configure_form = ConfigurePort()
    control_form = ControlTableForm()

    if configure_form.configure_submit.data and configure_form.validate_on_submit():
        global client
        print("configure_form validated!")
        port = configure_form.port.data
        print("Port: {}".format(port))
        baudrate = int(configure_form.baudrate.data)
        print("Baudrate: {}".format(baudrate))
        client = configure_client(port, baudrate)
        print("Client: {}".format(client))

    if control_form.control_submit.data and control_form.validate_on_submit():
        print("move_form validated!")
        print("Client: {}".format(client))
        x_axis = control_form.x_axis.data
        y_axis = control_form.y_axis.data
        move_type = request.form["move_type"]
        print("X: {}".format(x_axis))
        print("Y: {}".format(y_axis))
        print("Tipo de movimento: {}".format(move_type))

        try:
            move_by_point(x_axis, y_axis, client)
        except ConnectionException:
            flash("Erro ao tentar conectar", "error")

    return render_template(
        "home.html", title="home", configure_form=configure_form, move_form=control_form
    )


@app.route("/data", methods=["GET", "POST"])
def data():
    """Rota - Data"""

    # Data Format
    # [TIME, Eixo_x, Eixo_y]

    Eixo_x = random() * 100
    Eixo_y = random() * 55

    dados = [time() * 1000, Eixo_x, Eixo_y]

    response = make_response(json.dumps(dados))

    response.content_type = "application/json"

    return response


@app.route("/graphic", methods=["GET", "POST"])
def graphic():
    return render_template("graphic.html")


@app.route("/register", methods=["GET", "POST"])
@login_required
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

    return render_template("register.html", title="Cadastro", form=form)


@app.route("/log")
def log():
    """Rota - Histórico"""

    return render_template("log.html", title="Histórico")


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
