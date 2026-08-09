"""Centralized error handling middleware."""
import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application error."""
    def __init__(self, message, status_code=400, error_details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_details = error_details


class ValidationError(AppError):
    """Validation error."""
    def __init__(self, message, error_details=None):
        super().__init__(message, 400, error_details)


class AuthenticationError(AppError):
    """Authentication error."""
    def __init__(self, message="Authentication required"):
        super().__init__(message, 401)


class AuthorizationError(AppError):
    """Authorization error."""
    def __init__(self, message="Access denied"):
        super().__init__(message, 403)


class NotFoundError(AppError):
    """Resource not found error."""
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class ConflictError(AppError):
    """Resource conflict error."""
    def __init__(self, message="Resource already exists"):
        super().__init__(message, 409)


def register_error_handlers(app):
    """
    Register global error handlers.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(AppError)
    def handle_app_error(error):
        """Handle custom application errors."""
        logger.warning(f"Application error: {error.message}", exc_info=True)
        return jsonify({
            'success': False,
            'data': None,
            'message': error.message,
            'error': error.error_details
        }), error.status_code
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP error {error.code}: {error.description}")
        return jsonify({
            'success': False,
            'data': None,
            'message': error.description,
            'error': error.name
        }), error.code
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """Handle database errors."""
        logger.error(f"Database error: {str(error)}", exc_info=True)
        return jsonify({
            'success': False,
            'data': None,
            'message': "Database error occurred",
            'error': "Please try again later"
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors."""
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return jsonify({
            'success': False,
            'data': None,
            'message': "An unexpected error occurred",
            'error': "Please try again later"
        }), 500
    
    logger.info("Error handlers registered")
