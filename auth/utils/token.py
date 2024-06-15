'''To work with jwt'''
from datetime import datetime, timezone
from flask_jwt_extended import decode_token

def is_token_expired(token):
    '''Check if token is expired'''
    decoded_token = decode_token(token)
    if not decoded_token:
        return True
    exp_timestamp = decoded_token.get('exp')
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    return exp_datetime < datetime.now(tz=timezone.utc)
