import jwt
from datetime import datetime, timedelta

from core.settings import SECRET_KEY

def generate_jwt_token(email):
    token = jwt.encode({
                'email': email,
                'exp': datetime.now() + timedelta(minutes=10)
            }, key=SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
