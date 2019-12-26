import base64

import pytest
from flask import Flask
from werkzeug.security import generate_password_hash

from Lost_And_Found.config import TestingConfig
from Lost_And_Found.app import create_app, db
from Lost_And_Found.app.models.models import users, items

@pytest.fixture(scope="module")
def app_client():

    flask_app = create_app(TestingConfig)
    db.init_app(flask_app)
    app_context = flask_app.test_request_context()
    app_context.push()
    flask_app.config.from_object(TestingConfig)
    flask_app.testing = True
    client = flask_app.test_client()
    print("app......")
    with flask_app.app_context():
        from Lost_And_Found.app.user import userbp
        from Lost_And_Found.app.item import itembp

        flask_app.register_blueprint(userbp)
        flask_app.register_blueprint(itembp)
        from Lost_And_Found.app.models.models import users, items

        db.create_all()
        yield client
        db.drop_all()


@pytest.fixture(scope="module")
def new_user(app_client):
    user = users("zib77707@eveav.com", generate_password_hash("123456"), 1)
    db.session.add(user)
    db.session.commit()


@pytest.fixture(scope="function", autouse=True)
def get_token(app_client):
    usrPass = "zib77707@eveav.com:123456"
    data_bytes = usrPass.encode("utf-8")
    b64Val = base64.b64encode(data_bytes)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic %s" % b64Val.decode("utf-8"),
    }
    payload = ""
    response = app_client.get("/user/login", data=payload, headers=headers)
    return response.json
