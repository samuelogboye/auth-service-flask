from flask_jwt_extended import decode_token
from datetime import datetime, timezone

def decode_jwt(token):
    try:
        decoded_token = decode_token(token)
        return decoded_token
    except Exception as e:
        return None

def is_token_expired(token):
    decoded_token = decode_jwt(token)
    if not decoded_token:
        return True
    exp_timestamp = decoded_token.get('exp')
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    return exp_datetime < datetime.now(tz=timezone.utc)
