from flask import render_template, flash, url_for, redirect
from flaskr import app
from .forms import RegistrationForm, LoginForm, ForgotForm

# from .models import Users, Positions


@app.route("/")
@app.route("/home")
def home():
    """Rota - Principal"""

    return render_template("home.html", title="home")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Rota - Login"""

    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@admin.com" and form.password.data == "admin":
            flash("Acesso permitido!", "success")
            return redirect(url_for("home"))
        else:
            flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Rota - Register"""

    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Conta criada para {form.name.data}.", "success")

    return render_template("register.html", title="Cadastro", form=form)


@app.route("/forgot")
def forgot():
    """Rota - Esqueceu a senha"""

    form = ForgotForm()

    return render_template("forgot.html", title="Esqueceu a senha?", form=form)
