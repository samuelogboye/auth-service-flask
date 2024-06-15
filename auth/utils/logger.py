'''Implement Logger service'''
import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    handlers=[RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=10)],
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Custom logger
logger = logging.getLogger('app_logger')

def log_error(function_name, message):
    '''Logs Error'''
    logger.error("%s - %s", function_name, message)

def log_success(function_name, message):
    '''Logs Success'''
    logger.info("%s - %s", function_name, message)

def log_warning(function_name, message):
    '''Logs Warning'''
    logger.warning("%s - %s", function_name, message)

def log_debug(function_name, message):
    '''Logs Debug'''
    logger.debug("%s - %s", function_name, message)

def log_route(func):
    '''Logs route requests'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
        except (RuntimeError, ValueError):
            user_id = None

        response, status = func(*args, **kwargs)
        user_info = f"User ID: {user_id} - " if user_id else ""
        ip_address = request.remote_addr
        message = response.get('message') or response.get('msg') or 'No message provided'
        if 200 <= status < 300:
            log_success(func.__name__, f"{ip_address}{user_info}{message}")
        else:
            log_error(func.__name__, f"{ip_address}{user_info}{message}")
        return jsonify(response), status
    return wrapper
