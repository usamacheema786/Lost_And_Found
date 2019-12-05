from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Flask
from config_default import ProductionConfig


def create_app(config_object=ProductionConfig):

    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    return app


app = create_app(ProductionConfig)
mail = Mail(app)
db = SQLAlchemy(app)


if __name__ == "__main__":
    from app.user import userbp
    from app.item import itembp
    app.register_blueprint(userbp)
    app.register_blueprint(itembp)

    app.run(host="0.0.0.0", debug=True)
