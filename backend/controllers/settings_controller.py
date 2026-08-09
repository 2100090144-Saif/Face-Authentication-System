"""Settings controller."""
import logging
from flask import request
from flask_login import current_user, login_required
from backend.services import AuthService, FaceService
from backend.utils import (
    success_response,
    error_response,
    validation_error_response
)

logger = logging.getLogger(__name__)


class SettingsController:
    """Controller for settings endpoints."""
    
    @staticmethod
    @login_required
    def get_settings():
        """Get user settings."""
        try:
            face_service = FaceService()
            encodings = face_service.get_user_encodings(current_user)
            
            return success_response(
                data={
                    'face_recognition_enabled': current_user.face_recognition_enabled,
                    'has_face_encodings': len(encodings) > 0,
                    'encoding_count': len(encodings)
                },
                message='Settings retrieved'
            )
        
        except Exception as e:
            logger.error(f"Error in get_settings: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
    
    @staticmethod
    @login_required
    def update_face_recognition():
        """Update face recognition setting."""
        try:
            data = request.get_json()
            
            if not data or 'enabled' not in data:
                return validation_error_response('enabled field is required')
            
            enabled = data.get('enabled')
            
            if not isinstance(enabled, bool):
                return validation_error_response('enabled must be a boolean')
            
            # Update setting
            success, error = AuthService.update_face_recognition_setting(current_user, enabled)
            
            if error:
                return error_response('Failed to update settings', error, 500)
            
            return success_response(
                data={'face_recognition_enabled': enabled},
                message='Face recognition settings updated'
            )
        
        except Exception as e:
            logger.error(f"Error in update_face_recognition: {str(e)}", exc_info=True)
            return error_response('Internal server error', 'An unexpected error occurred', 500)
