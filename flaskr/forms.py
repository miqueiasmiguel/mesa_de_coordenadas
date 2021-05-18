from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    """Formulário para o cadastro de usuários"""

    user_type = RadioField(
        "Tipo do usuário", choices=["Comum", "Especial"], validators=[DataRequired()]
    )
    name = StringField("Nome", validators=[DataRequired()])
    registration_number = StringField("Matrícula", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirmar a senha", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Cadastrar")


class LoginForm(FlaskForm):
    """Formulário para Login"""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lermbrar")
    submit = SubmitField("Entrar")


class ForgotForm(FlaskForm):
    """Formulário para recuperação de senha"""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Entrar")
