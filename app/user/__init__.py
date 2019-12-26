from flask import Blueprint
userbp = Blueprint('user', __name__)


try:
    from Lost_And_Found.app.user import api
except ImportError:
    from app.user import api
