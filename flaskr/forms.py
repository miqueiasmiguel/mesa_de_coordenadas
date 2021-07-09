from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.fields.simple import FileField
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
    submit = SubmitField("Entrar", id="btn-login")


class ForgotForm(FlaskForm):
    """Formulário para recuperação de senha"""

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Entrar")


class ConfigurePort(FlaskForm):
    """Formulário para configurar a porta"""

    choices = []
    for number in range(1, 11):
        choices.append(("COM{}".format(number), "COM{}".format(number)))

    port = SelectField("Porta:", choices=choices)
    baudrate = SelectField("Baud:", choices=[("9600", "9600"), ("19200", "19200")])
    submit = SubmitField("Conectar")


class MoveTableForm(FlaskForm):
    """Formulário para movimentar a mesa"""

    move_type = RadioField(
        "Tipo de movimento:", id="move_type", choices=["by_point", "by_trajectory"]
    )
    x_axis = IntegerField("X:", id="x-axis")
    y_axis = IntegerField("Y:", id="y-axis")
    trajectory = FileField("Abrir", id="import-trajectory")
    submit = SubmitField("Iniciar", id="start-btn")
