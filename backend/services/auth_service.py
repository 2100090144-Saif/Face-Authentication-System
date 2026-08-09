"""Authentication service."""
import logging
from backend.app import db
from backend.models import User

logger = logging.getLogger(__name__)


class AuthService:
    """Service for user authentication operations."""
    
    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user.
        
        Args:
            username: User's username
            email: User's email
            password: User's password (plain text)
        
        Returns:
            Tuple of (user, error_message)
        """
        try:
            # Validate username
            valid, error = User.validate_username(username)
            if not valid:
                return None, error
            
            # Validate email
            valid, error = User.validate_email(email)
            if not valid:
                return None, error
            
            # Validate password
            valid, error = User.validate_password(password)
            if not valid:
                return None, error
            
            # Check if username exists
            if User.query.filter_by(username=username).first():
                return None, "Username already exists"
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                return None, "Email already exists"
            
            # Create user
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"User registered: {username}")
            return user, None
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user: {str(e)}")
            return None, "Registration failed"
    
    @staticmethod
    def login_user(username, password):
        """
        Authenticate user with username and password.
        
        Args:
            username: User's username
            password: User's password
        
        Returns:
            Tuple of (user, error_message)
        """
        try:
            # Find user
            user = User.query.filter_by(username=username).first()
            
            if not user:
                logger.warning(f"Login failed: user not found ({username})")
                return None, "Invalid username or password"
            
            # Check password
            if not user.check_password(password):
                logger.warning(f"Login failed: invalid password ({username})")
                return None, "Invalid username or password"
            
            logger.info(f"User logged in: {username}")
            return user, None
        
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return None, "Login failed"
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        try:
            return User.query.get(user_id)
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username."""
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    @staticmethod
    def update_face_recognition_setting(user, enabled):
        """
        Update face recognition setting for user.
        
        Args:
            user: User object
            enabled: Boolean
        
        Returns:
            Tuple of (success, error_message)
        """
        try:
            user.face_recognition_enabled = enabled
            db.session.commit()
            
            logger.info(f"Face recognition {'enabled' if enabled else 'disabled'} for user {user.username}")
            return True, None
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating face recognition setting: {str(e)}")
            return False, "Failed to update settings"
