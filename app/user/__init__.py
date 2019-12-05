from flask import Blueprint
userbp = Blueprint('user', __name__)

from app.user.api import *
