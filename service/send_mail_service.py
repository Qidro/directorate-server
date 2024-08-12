import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

smtp_port = os.environ.get('SMTP_PORT')
smtp_server = os.environ.get('SMTP_SERVER')
smtp_username = os.environ.get('SMTP_USERNAME')
smtp_password = os.environ.get('SMTP_PASSWORD')


def create_smtp_connect():
    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
    except smtplib.SMTPException as error:
        raise error

    return smtp_connection


def send_email(smtp_connection, to_address, subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = Header(smtp_username, 'utf-8')
    msg['To'] = Header(to_address, 'utf-8')
    smtp_connection.sendmail(smtp_username, to_address, msg.as_string())
