from celery import Celery
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# from config import ProductionConfig

mail = Mail()
db = SQLAlchemy()
app = Flask(__name__)
# app.config.from_object('config.ProductionConfig')
mail.init_app(app)
db.init_app(app)
db.app = app


def create_app(prod):
    app = Flask(__name__)
    app.config.from_object(prod)

    mail.init_app(app)
    db.init_app(app)
    db.app = app

    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend = app.config['CELERY_RESULT_BACKEND'],
        broker = app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

