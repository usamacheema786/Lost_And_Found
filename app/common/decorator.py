import jwt

from flask import request,jsonify,current_app
from functools import wraps

from werkzeug.exceptions import BadRequest
from werkzeug.routing import ValidationError

from app.models.models import users
from run import app


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token =None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({'message':'Token is miising'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = users.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message':'Invalid token'}),401

        return f(current_user,*args,**kwargs)
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


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, current_app.config[schema_name])
            except ValidationError as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)
        return wrapper
    return decorator
