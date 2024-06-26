# pylint: disable-all
from flask import Blueprint, jsonify
from pydantic import ValidationError
from auth.utils.logger import log_route

error = Blueprint("error", __name__)


class CustomError(Exception):
    """Exception class for custom errors"""

    def __init__(self, error, code, message):
        """constructor for custom error class

        Args:
            error (_type_): Error Name
            code (_type_): HTTP error code
            message (_type_): error message
        """
        self.error = error
        self.code = code
        self.message = message



@error.app_errorhandler(CustomError)
@log_route
def custom_error(error):
    """app error handler for custom errors"""
    return (
        {"error": error.error, "message": error.message},
        error.code,
    )

@error.app_errorhandler(ValidationError)
@log_route
def raise_validation_error(error):
    """app error handler for pydantic validation errors"""
    msg = [
        {"field": err["loc"][0], "error": err["msg"]} for err in error.errors()
    ]
    return (
        {"error": "Bad Request", "message": msg},
        400,
    )

@error.app_errorhandler(400)
@log_route
def bad_request(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": error.description}, 400


@error.app_errorhandler(401)
@log_route
def Unauthorized(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": error.description}, 401


@error.app_errorhandler(403)
@log_route
def Forbidden(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": error.description}, 403


@error.app_errorhandler(404)
@log_route
def resource_not_found(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": error.description}, 404


@error.app_errorhandler(405)
@log_route
def method_not_allowed(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (
        {"error": error.name, "message": error.description},
        405,
    )


@error.app_errorhandler(422)
@log_route
def cant_process(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": error.description}, 422


# pylint: disable=function-redefined
@error.app_errorhandler(429)
@log_route
def cant_process(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": error.description}, 429


@error.app_errorhandler(500)
@log_route
def server_error(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return {"error": error.name, "message": "Something went wrong"}, 500