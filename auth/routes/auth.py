'''Contains the route and its business logic call to authservice'''
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flasgger import swag_from
from auth.utils.logger import log_route
from ..services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

# test endpoint
@auth_bp.route('/test', methods=['GET'])
@log_route
def test():
    """
    A test route
    ---
    responses:
      200:
        description: Test endpoint successful
        examples:
          application/json:
            message: Test endpoint
    """
    return {'message': 'Test endpoint'}, 200


@auth_bp.route('/register', methods=['POST'])
@log_route
def register():
    """
    Endpoint to register a user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            email:
              type: string
            password:
              type: string
          required:
            - username
            - email
            - password
    tags:
      - auth
    responses:
      201:
        description: User registered successfully
        examples:
          application/json:
            message: User registered successfully
      400:
        description: Missing required fields or validation errors
        examples:
          application/json:
            message: Email already exists
    """
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
    """
    Endpoint to login a user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
          required:
            - email
            - password
    tags:
      - auth
    responses:
      200:
        description: User logged in successfully
        examples:
          application/json:
            access_token: string
            refresh_token: string
            message: User logged in successfully
      400:
        description: Missing required fields
        examples:
          application/json:
            message: Missing required fields
      401:
        description: Invalid credentials
        examples:
          application/json:
            message: Invalid credentials
    """
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
    """
    Endpoint to reset password
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            new_password:
              type: string
          required:
            - new_password
    security:
      - Bearer: []
    tags:
      - auth
    responses:
      200:
        description: Password updated successfully
        examples:
          application/json:
            message: Password updated successfully
      400:
        description: Missing required fields or validation errors
        examples:
          application/json:
            message: Missing required fields
    """
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
    """
    Endpoint to change password
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            current_password:
              type: string
            new_password:
              type: string
          required:
            - current_password
            - new_password
    security:
      - Bearer: []
    tags:
      - auth
    responses:
      200:
        description: Password updated successfully
        examples:
          application/json:
            message: Password updated successfully
      400:
        description: Missing required fields or validation errors
        examples:
          application/json:
            message: Missing required fields
      401:
        description: Invalid current password
        examples:
          application/json:
            message: Invalid current password
    """
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
    """
    Endpoint to refresh access token
    ---
    security:
      - Bearer: []
    tags:
      - auth
    responses:
      200:
        description: Tokens refreshed successfully
        examples:
          application/json:
            access_token: string
            refresh_token: string
            message: Tokens refreshed successfully
      401:
        description: Invalid token
        examples:
          application/json:
            message: Invalid token
    """
    current_user = get_jwt_identity()
    jti = get_jwt()['jti']
    # Extract the token from the header
    refresh_token = request.headers.get('Authorization').split()[1]
    user_info = {'sub': current_user, 'jti': jti, 'token': refresh_token}
    response, status = AuthService.refresh_token(user_info)
    return response, status
