from unittest import TestCase

import pytest

# from flask import Flask
# from flask import current_app
# from flask_sqlalchemy import SQLAlchemy
# from app.config import config
# from app import db
from Lost_And_Found.config import TestingConfig
from Lost_And_Found.app import app


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object(TestingConfig)
        return app

    # def setUp(self):
    #
    #     db.create_all()
    #     db.session.commit()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
