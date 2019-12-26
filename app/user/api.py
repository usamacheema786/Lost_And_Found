import datetime
import jwt
import re

from flask import request, jsonify, make_response, url_for
from werkzeug.security import check_password_hash, generate_password_hash
try:
    from app.common.decorator import token_required, validate_json, validate_schema
    from app.common.schema import user_schema
    from app.emailverify.emailverify import send_async_email
    from app.emailverify.token import generate_confirmation_token, confirm_token
    from app.models.models import users
    from app.user import userbp
    from app import db
    from run import app
except ImportError:
    from Lost_And_Found.app.common.decorator import token_required, validate_json, validate_schema
    from Lost_And_Found.app.common.schema import user_schema
    from Lost_And_Found.app.emailverify.emailverify import send_async_email
    from Lost_And_Found.app.emailverify.token import generate_confirmation_token, confirm_token
    from Lost_And_Found.app.models.models import users
    from Lost_And_Found.app.user import userbp
    from Lost_And_Found.app import db
    from Lost_And_Found.run import app


@userbp.route("/user/register", methods=["POST"])
@validate_json
@validate_schema(user_schema)
def register_user():
    """function to register user """
    data = request.get_json()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({"message": "provide correct email "}), 400
    user = users.query.filter_by(email=data["email"]).first()
    con = str(user.confirmed)
    if not user:
        hash_password = generate_password_hash(data["password"])
        new_user = users(email=data["email"], password=hash_password, confirmed=0)
        db.session.add(new_user)
        db.session.commit()
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for("user.confirm_email", token=token, _external=True)
        subject = "Please confirm your email"
        send_async_email.delay(new_user.email, subject, confirm_url)
        return jsonify({"message": "A confirmation email has been sent via email"}), 200
    return jsonify({"message": "Email already registered "+con}), 409


@userbp.route("/change_password", methods=["PUT"])
@token_required
def change_password(current_user):
    """function to change user password"""
    if not current_user:
        return jsonify({"message": "please login first to perform this operation"}), 401
    data = request.get_json()
    if data["password"] != "":
        hashed_pass = generate_password_hash(data["password"])
        current_user.password = hashed_pass
        db.session.commit()
        return jsonify({"message": "password changed successfully"}), 200
    return jsonify({"message": "password field is required"}), 400


@userbp.route("/user/login")
def login():
    """function to login by user"""
    auth_data = request.authorization
    if not auth_data or not auth_data.username or not auth_data.password:
        return make_response(
            "incorrect login detail1",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required"'},
        )
    user = users.query.filter_by(email=auth_data.username).first()
    if not user:
        return jsonify({"message": "email does not exist "}),401
    if check_password_hash(user.password, auth_data.password):
        if user.confirmed:
            token = generate_confirmation_token(str(user.id))
            return jsonify({"token": token.decode("UTF-8")}), 200
        else:
            return jsonify({"message": "please confirm your email before login"}),401
    return jsonify({"message": "incorrect password"}),401


@userbp.route("/confirm/<token>")
def confirm_email(token):
    """function to confirm email """
    try:
        email = confirm_token(token)
    except ValueError:
        return jsonify({"message": "The confirmation link is invalid or has expired"})
    user = users.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify({"message": "Account already confirmed. Please login."}) ,409
    else:
        user.confirmed = 1
        db.session.add(user)
        db.session.commit()
        return jsonify(
            {"message": "Thanks for confirming the email !you can login now"}, 200
        )
