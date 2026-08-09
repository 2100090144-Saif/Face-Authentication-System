"""Face recognition controller."""
import logging
from flask import request
from flask_login import login_user, current_user, login_required
from backend.services.face_service import get_face_service
from backend.utils import (
    success_response,
    error_response,
    created_response,
    unauthorized_response,
    validation_error_response
)
from backend.middleware.rate_limiter import rate_limit_face_auth

logger = logging.getLogger(__name__)


class FaceController:
    """Controller for face recognition endpoints."""
    
    @staticmethod
    @login_required
    def register_face():
        """Register user's face."""
        try:
            # Get singleton face service
            face_service = get_face_service()
            
            # Check if image file is present
            if 'image' not in request.files:
                return validation_error_response('Image file is required')
            
            file = request.files['image']
            
            if file.filename == '':
                return validation_error_response('Please select an image file')
            
            # Read image bytes
            image_bytes = file.read()
            
            # Register face
            face_encoding, error = face_service.register_face(current_user, image_bytes)
            
            if error:
                return error_response('Face registration failed', error)
            
            return created_response(
                data={
                    'encoding_id': face_encoding.id,
                    'message': 'Face registered successfully'
                },
                message='Face registration successful'
            )
        
        except Exception as e:
            logger.error(f"Error in register_face: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    @rate_limit_face_auth(max_attempts=5, window=60)
    def login_face():
        """Login using face recognition with rate limiting and strict security."""
        try:
            # SECURITY: Clear any existing session before authentication
            # This prevents session fixation attacks
            from flask import session
            session.clear()
            logger.info("Session cleared before face authentication")
            
            # Get singleton face service
            face_service = get_face_service()
            
            print(request.files)
            
            # Check if image file is present
            if 'image' not in request.files:
                logger.warning("Face login attempt with no image file")
                return validation_error_response('Image file is required')
            
            file = request.files['image']
            
            if file.filename == '':
                logger.warning("Face login attempt with empty filename")
                return validation_error_response('Please select an image file')
            
            # Read image bytes
            image_bytes = file.read()
            
            if not image_bytes or len(image_bytes) == 0:
                logger.warning("Face login attempt with empty image data")
                return validation_error_response('Image data is empty')
            
            # Authenticate face - CRITICAL: This returns (user, confidence, error)
            user, confidence, error = face_service.authenticate_face(image_bytes)
            
            # SECURITY CHECK 1: Check if error occurred
            if error:
                logger.warning(f"Face authentication failed: {error}")
                return unauthorized_response(f'Face authentication failed: {error}')
            
            # SECURITY CHECK 2: Verify user object is not None
            if user is None:
                logger.error("CRITICAL: Face authentication returned no error but user is None")
                return unauthorized_response('Face authentication failed: No user matched')
            
            # SECURITY CHECK 3: Verify confidence is above threshold (60%)
            # This is the CRITICAL security gate - must be >= 60% confidence
            # Note: confidence is now returned as percentage (0-100), not decimal (0-1)
            if confidence < 60.0:
                logger.warning(f"Face authentication rejected: confidence {confidence:.1f}% below threshold 60%")
                return unauthorized_response(f'Face authentication failed: Confidence too low ({confidence:.1f}%)')
            
            # SECURITY CHECK 4: Verify user has face recognition enabled
            if not user.face_recognition_enabled:
                logger.warning(f"Face authentication rejected: face recognition disabled for user {user.username}")
                return unauthorized_response('Face authentication failed: Face recognition not enabled')
            
            # All checks passed - log user in
            logger.info(f"✅ Face authentication SUCCESSFUL: {user.username} (confidence={confidence:.1f}%)")
            login_user(user, remember=True)
            
            return success_response(
                data={
                    'user': user.to_dict(),
                    'confidence': float(confidence)
                },
                message='Face authentication successful'
            )
        
        except Exception as e:
            logger.error(f"Error in login_face: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    @login_required
    def get_encodings():
        """Get user's face encodings."""
        try:
            face_service = get_face_service()
            encodings = face_service.get_user_encodings(current_user)
            
            return success_response(
                data={'encodings': [enc.to_dict() for enc in encodings]},
                message='Encodings retrieved'
            )
        
        except Exception as e:
            logger.error(f"Error in get_encodings: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    @login_required
    def delete_encodings():
        """Delete user's face encodings."""
        try:
            face_service = get_face_service()
            count, error = face_service.delete_user_encodings(current_user)
            
            if error:
                return error_response('Failed to delete encodings', error, 500)
            
            return success_response(
                data={'deleted_count': count},
                message='Face encodings deleted'
            )
        
        except Exception as e:
            logger.error(f"Error in delete_encodings: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
