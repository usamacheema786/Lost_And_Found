import datetime
import jwt
try:
    from run import app
except ImportError:
    from Lost_And_Found.run import app


def generate_confirmation_token(email):
    token = jwt.encode({'email': str(email), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return token


def confirm_token(token):
    data = jwt.decode(token, app.config['SECRET_KEY'])
    current_user = data['email']
    return current_user
