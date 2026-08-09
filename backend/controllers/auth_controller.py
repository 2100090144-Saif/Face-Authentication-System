"""Authentication controller."""
import logging
from flask import request
from flask_login import login_user, logout_user, current_user
from backend.services import AuthService
from backend.utils import (
    success_response,
    error_response,
    created_response,
    unauthorized_response,
    validation_error_response
)

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication endpoints."""
    
    @staticmethod
    def register():
        """Register a new user."""
        try:
            data = request.get_json()
            
            if not data:
                return validation_error_response('Request body is required')
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not username or not email or not password:
                return validation_error_response('Username, email, and password are required')
            
            # Register user
            user, error = AuthService.register_user(username, email, password)
            
            if error:
                return error_response('Registration failed', error)
            
            # Log user in
            login_user(user, remember=True)
            
            return created_response(
                data={'user': user.to_dict()},
                message='Registration successful'
            )
        
        except Exception as e:
            logger.error(f"Error in register: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    def login():
        """Login with username and password."""
        try:
            data = request.get_json()
            
            if not data:
                return validation_error_response('Request body is required')
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return validation_error_response('Username and password are required')
            
            # Authenticate user
            user, error = AuthService.login_user(username, password)
            
            if error:
                return unauthorized_response('Login failed')
            
            # Log user in
            login_user(user, remember=True)
            
            return success_response(
                data={'user': user.to_dict()},
                message='Login successful'
            )
        
        except Exception as e:
            logger.error(f"Error in login: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    def logout():
        """Logout current user."""
        try:
            logout_user()
            return success_response(message='Logout successful')
        
        except Exception as e:
            logger.error(f"Error in logout: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    def get_current_user():
        """Get current user information."""
        try:
            if not current_user.is_authenticated:
                return unauthorized_response('Please login to access this resource')
            
            return success_response(
                data={'user': current_user.to_dict()},
                message='User retrieved'
            )
        
        except Exception as e:
            logger.error(f"Error in get_current_user: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
