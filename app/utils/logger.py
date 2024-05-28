import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
from flask import jsonify
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
    logger.error(f"{function_name} - {message}")

def log_success(function_name, message):
    logger.info(f"{function_name} - {message}")

# Optional: You can add more custom log functions as needed
def log_warning(function_name, message):
    logger.warning(f"{function_name} - {message}")

def log_debug(function_name, message):
    logger.debug(f"{function_name} - {message}")

def log_route(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
        except Exception:
            user_id = None

        response, status = func(*args, **kwargs)
        user_info = f"User ID: {user_id} - " if user_id else ""
        message = response.get('message') or response.get('msg') or 'No message provided'
        if status >= 200 and status < 300:
            log_success(func.__name__, f"{user_info}{message}")
        else:
            log_error(func.__name__, f"{user_info}{message}")
        return jsonify(response), status
    return wrapper
