from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flaskr.models import Users


class RegistrationForm(FlaskForm):
    """Formulário para o cadastro de usuários"""

    user_type = RadioField(
        "Tipo do usuário", choices=["Comum", "Especial"], validators=[DataRequired()]
    )
    name = StringField("Nome", validators=[DataRequired()])
    reg_number = StringField("Matrícula", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirmar a senha", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Cadastrar")

    def validate_email(self, email):
        """
        Função para verificar se o
        banco de dados já possui um
        usuário com o mesmo e-mail
        """
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Um usuário já possui este e-mail")

    def validate_reg_number(self, reg_number):
        """
        Função para verificar se o
        banco de dados já possui um
        usuário com a mesma matrícula
        """
        user = Users.query.filter_by(reg_number=reg_number.data).first()
        if user:
            raise ValidationError("Um usuário já possui esta matrícula")


class LoginForm(FlaskForm):
    """Formulário para Login"""

    reg_number = StringField("Matícula:", validators=[DataRequired()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class ForgotForm(FlaskForm):
    """Formulário para recuperação de senha"""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Entrar")
