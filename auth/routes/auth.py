'''Contains the route and its business logic call to authservice'''
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.auth_service import AuthService
from auth.utils.logger import log_route

auth_bp = Blueprint('auth', __name__)

# test endpoint
@auth_bp.route('/test', methods=['GET'])
@log_route
def test():
    '''A test route'''
    return {'message': 'Test endpoint'}, 200


# Endpoint to register a user
@auth_bp.route('/register', methods=['POST'])
@log_route
def register():
    '''Endpoint to register a user'''
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return {'message': 'Missing required fields'}, 400

    username = data['username']
    email = data['email']
    password = data['password']

    response, status = AuthService.register_user(username, email, password)
    return response, status

@auth_bp.route('/login', methods=['POST'])
@log_route
def login():
    '''Endpoint to login a user'''
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return {'message': 'Missing required fields'}, 400

    email = data['email']
    password = data['password']

    response, status = AuthService.authenticate_user(email, password)
    return response, status

@auth_bp.route('/reset-password', methods=['POST'])
@jwt_required()
@log_route
def reset_password():
    '''Endpoint to reset password'''
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('new_password'):
        return {'message': 'Missing required fields'}, 400

    new_password = data['new_password']

    response, status = AuthService.update_password(user_id, new_password)
    return response, status

# Endpoint to change password
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@log_route
def change_password():
    '''Endpoint to change password'''
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('current_password') or not data.get('new_password'):
        return {'message': 'Missing required fields'}, 400

    current_password = data['current_password']
    new_password = data['new_password']

    response, status = AuthService.change_password(user_id, current_password, new_password)
    return response, status

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@log_route
def refresh():
    '''Endpoint to refresh access token'''
    current_user = get_jwt_identity()
    response, status = AuthService.refresh_token(current_user)
    return response, status
