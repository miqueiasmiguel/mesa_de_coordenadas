from flask import Flask, render_template, flash, url_for
from werkzeug.utils import redirect
from forms import RegistrationForm, LoginForm, ForgotForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "26bea9fc38afd17bd034bf4234e4f6fb"


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


if __name__ == "__main__":
    app.run(debug=True)
