from celery import Celery
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import ProductionConfig


def create_app(config_object=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
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


app = create_app(ProductionConfig)
mail = Mail(app)
db = SQLAlchemy(app)


if __name__ == "__main__":
    from app.user import userbp
    from app.item import itembp

    app.register_blueprint(userbp)
    app.register_blueprint(itembp)

    app.run(host="0.0.0.0", debug=True)
