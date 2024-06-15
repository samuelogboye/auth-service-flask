'''AuthService with business logic for the auth routes'''
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from auth import db
from auth.models.models import User
from auth.utils.validation import validate_email, validate_password, validate_username

PASSWORD_VALIDATION_ERROR = 'Password must be at least 8 char, at least one letter and one number'

class AuthService:
    '''Contains the business logic for the auth routes'''
    @staticmethod
    def register_user(username, email, password):
        '''Registers a new user'''
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400

        if not validate_email(email):
            return {'message': 'Invalid email address'}, 400

        if not validate_password(password):
            return {
                'message': PASSWORD_VALIDATION_ERROR 
                }, 400

        if not validate_username(username):
            return {
                'message': 'Username can only contain alphanumeric characters and underscores'
                }, 400

        # hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        new_user.insert()
        return {'message': 'User registered successfully'}, 201

    @staticmethod
    def authenticate_user(email, password):
        '''Authenticate a user'''
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
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
        '''Updates a user's password'''
        if not validate_password(new_password):
            return {
                'message': PASSWORD_VALIDATION_ERROR 
                }, 400
        user = User.query.get(user_id)
        user.set_password(new_password)
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200

    @staticmethod
    def change_password(user_id, current_password, new_password):
        '''Changes a user's password'''
        if not validate_password(new_password):
            return {
                'message': PASSWORD_VALIDATION_ERROR 
                }, 400
        user = User.query.get(user_id)
        if not user.check_password(current_password):
            return {'message': 'Invalid current password'}, 401
        user.set_password(new_password)
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200

    @staticmethod
    def refresh_token(current_user):
        '''Refreshes the access token'''
        access_token = create_access_token(
            identity=current_user,
            expires_delta=timedelta(minutes=15)
            )
        return {'access_token': access_token, 'message': 'Token refreshed Successfully'}, 200
