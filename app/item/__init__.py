from flask import Blueprint
itembp = Blueprint('item',__name__)

try:
    from app.item import api
except:
    from Lost_And_Found.app.item import api
