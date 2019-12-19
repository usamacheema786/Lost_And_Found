from flask_mail import Message

from run import app
from app import mail, make_celery

celery = make_celery(app)


@celery.task
def send_async_email(email, subject, link):
    """Background task to send an email with Flask-Mail."""
    msg = Message(subject,
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email],
                  html=link)
    msg.body = "Your confirmation link is here: "
    with app.app_context():
        mail.send(msg)
