import json
from random import random
from time import time
from flask import render_template, flash, url_for, redirect, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import app, db, bcrypt
from .forms import ConfigurePort, MoveTableForm, RegistrationForm, LoginForm, ForgotForm
from .models import Users
from src.serial_modules import configure_client


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
    move_form = MoveTableForm()

    if configure_form.validate_on_submit():
        port = configure_form.port.data
        baudrate = int(configure_form.baudrate.data)
        client = configure_client(port, baudrate)
        client.connect()

    return render_template(
        "home.html", title="home", configure_form=configure_form, move_form=move_form
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
