"""Standardized API response utilities."""
from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    """
    Return standardized success response.
    
    Args:
        data: Response data (dict, list, or None)
        message: Human-readable success message
        status_code: HTTP status code (default 200)
    
    Returns:
        Flask JSON response tuple
    """
    response = {
        'success': True,
        'data': data,
        'message': message,
        'error': None
    }
    return jsonify(response), status_code


def error_response(message="Error occurred", error=None, status_code=400):
    """
    Return standardized error response.
    
    Args:
        message: Human-readable error message
        error: Technical error details (optional)
        status_code: HTTP status code (default 400)
    
    Returns:
        Flask JSON response tuple
    """
    response = {
        'success': False,
        'data': None,
        'message': message,
        'error': error
    }
    return jsonify(response), status_code


def created_response(data=None, message="Created successfully"):
    """Return 201 Created response."""
    return success_response(data, message, 201)


def unauthorized_response(message="Unauthorized"):
    """Return 401 Unauthorized response."""
    return error_response(message, "Authentication required", 401)


def forbidden_response(message="Forbidden"):
    """Return 403 Forbidden response."""
    return error_response(message, "Access denied", 403)


def not_found_response(message="Not found"):
    """Return 404 Not Found response."""
    return error_response(message, "Resource not found", 404)


def validation_error_response(errors):
    """Return 400 Bad Request with validation errors."""
    return error_response(
        message="Validation failed",
        error=errors,
        status_code=400
    )
