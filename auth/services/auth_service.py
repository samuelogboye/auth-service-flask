from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from auth import db
from auth.models.models import User
from auth.utils.validation import validate_email, validate_password, validate_username
from auth.utils.logger import log_route


class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400
        
        if not validate_email(email):
            return {'message': 'Invalid email address'}, 400
        
        if not validate_password(password):
            return {'message': 'Password must be at least 8 characters long with at least one letter and one number'}, 400
        
        if not validate_username(username):
            # log_error('auth_service/register_user', f'{username} Username can only contain alphanumeric characters and underscores')
            return {'message': 'Username can only contain alphanumeric characters and underscores'}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)

        new_user.insert()
        return {'message': 'User registered successfully'}, 201

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=10))
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(minutes=60))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'User logged in successfully'
        }, 200

    @staticmethod
    def update_password(user_id, new_password):
        if not validate_password(new_password):
            return {'message': 'Password must be at least 8 characters long with at least one letter and one number'}, 400
        user = User.query.get(user_id)
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200

    @staticmethod
    def change_password(user_id, current_password, new_password):
        if not validate_password(new_password):
            return {'message': 'Password must be at least 8 characters long with at least one letter and one number'}, 400
        user = User.query.get(user_id)
        if not check_password_hash(user.password_hash, current_password):
            return {'message': 'Invalid current password'}, 401
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200

    @staticmethod
    def refresh_token(current_user):
        access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=15))
        return {'access_token': access_token, 'message': 'Token refreshed Successfully'}, 200
    
