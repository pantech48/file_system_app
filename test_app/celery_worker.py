import smtplib
from celery import Celery

from email.mime.text import MIMEText
from config import Config
from app import app


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery


celery = make_celery(app)


@celery.task
def send_email_task(email_data):
    send_email(**email_data)


def send_email(subject, recipients, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = Config.MAIL_USERNAME
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        server.sendmail(Config.MAIL_USERNAME, recipients, msg.as_string())
