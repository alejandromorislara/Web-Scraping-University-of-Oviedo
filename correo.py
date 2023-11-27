import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from credentials import credentials_dict
import time

class EmailSender:
    # Path constante al directorio de archivos Excel de noticias
    NEWS_DIRECTORY = credentials_dict['path_excel_noticias']

    def __init__(self):
        self.smtp_server = 'smtp.office365.com'
        self.smtp_port = 587
        self.smtp_username = credentials_dict['username']
        self.smtp_password = credentials_dict['password']
        self.to_email = credentials_dict['to_mail']
        self.subject = 'Actualización de  las noticias semanales de la Universidad de Oviedo'
        self.body = 'Este correo se envió automáticamente. Si tiene algún problema, por favor, contáctenos.'

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = self.to_email
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.body, 'plain'))

        # Obtener el archivo más reciente en el directorio
        latest_file = max(os.listdir(self.NEWS_DIRECTORY), key=lambda x: os.path.getctime(os.path.join(self.NEWS_DIRECTORY, x)))
        attachment_path = os.path.join(self.NEWS_DIRECTORY, latest_file)

        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            time.sleep(1)
            server.sendmail(self.smtp_username, self.to_email, msg.as_string())

        print('El correo ha sido enviado correctamente')

