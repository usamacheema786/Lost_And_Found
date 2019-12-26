import jwt
import json

from flask import request, jsonify
from functools import wraps
from flask_expects_json import validate

from werkzeug.exceptions import BadRequest
from werkzeug.routing import ValidationError
try:
    from app.emailverify.token import confirm_token
    from app.models.models import users
    from run import app
except ImportError:
    from Lost_And_Found.app.emailverify.token import confirm_token
    from Lost_And_Found.app.models.models import users
    from Lost_And_Found.run import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "access-token" in request.headers:
            token = request.headers["access-token"]
        else:
            jsonify({'message':"token tag is missing"}),400
        if not token:
            return jsonify({"message": "Token is miising"}),401
        try:
            data = confirm_token(token)
            current_user = users.query.filter_by(id=data).first()
        except:
            return jsonify({"message": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)

    return wrapper


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                if request.json:
                    validate(request.json, schema)
                else:
                    validate(json.loads(request.form["data"]), schema)
            except ValidationError as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)

        return wrapper

    return decorator
