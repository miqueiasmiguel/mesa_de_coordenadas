import smtplib
from email.message import EmailMessage


class SendEmail:
    """Classe para enviar o e-mail de recuperação"""

    def send_email(self, user_email: str, user_password: str):
        """Envia um e-mail para o usuário contendo sua senha

        :param user_email: e-mail do usuário que solicitou a senha
        :param user_password: senha do usuário
        """

        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login("mesacoordenadasufpb@gmail.com", "informaticaindustrialalunos")

        msg = EmailMessage()
        msg.set_content(user_password)

        msg["Subject"] = "Senha da mesa de coordenadas"
        msg["From"] = "mesacoordenadasufpb@gmail.com"
        msg["To"] = f"{user_email}"

        server.send_message(msg)
        server.quit()
