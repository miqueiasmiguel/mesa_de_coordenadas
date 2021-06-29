from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from flaskr import app, db, bcrypt
from src.serial_modules import serial_ports
from .forms import RegistrationForm, LoginForm, ForgotForm
from .models import Users


@app.route("/home")
@login_required
def home():
    """Rota - Principal"""

    ports = serial_ports()
    return render_template("home.html", title="home", ports=ports)


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


@app.route("/logout")
def logout():
    """Rota - Logout"""

    logout_user()
    return redirect(url_for("login"))


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


@app.route("/forgot")
def forgot():
    """Rota - Esqueceu a senha"""

    form = ForgotForm()
    return render_template("forgot.html", title="Esqueceu a senha?", form=form)
