"""Health check controller."""
import logging
from flask import jsonify
from backend.app import db
from backend.utils.response import success_response, error_response

logger = logging.getLogger(__name__)

# Cache AI service health status to avoid repeated initializations
_ai_service_health_cached = None


class HealthController:
    """Controller for health check endpoints."""
    
    @staticmethod
    def health_check():
        """
        System health check.
        
        Checks:
        - Database connectivity
        - AI service availability
        - Application status
        """
        global _ai_service_health_cached
        
        health_status = {
            'status': 'healthy',
            'checks': {}
        }
        
        # Check database
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            health_status['checks']['database'] = 'healthy'
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            health_status['checks']['database'] = 'unhealthy'
            health_status['status'] = 'degraded'
        
        # Check AI service (use cached result to avoid repeated initializations)
        if _ai_service_health_cached is None:
            try:
                from backend.services.face_service import get_face_service
                # Get singleton instance (initializes only once)
                face_service = get_face_service()
                _ai_service_health_cached = {
                    'status': 'healthy',
                    'note': 'Face recognition service initialized'
                }
                logger.info("✅ AI service health check: healthy (singleton initialized)")
            except RuntimeError as e:
                # face_recognition not installed
                logger.warning(f"AI service check: {str(e)}")
                _ai_service_health_cached = {
                    'status': 'degraded',
                    'note': 'face_recognition library not installed'
                }
            except Exception as e:
                logger.error(f"AI service health check failed: {str(e)}")
                _ai_service_health_cached = {
                    'status': 'unhealthy',
                    'note': str(e)
                }
        
        health_status['checks']['ai_service'] = _ai_service_health_cached['status']
        if 'note' in _ai_service_health_cached:
            health_status['checks']['ai_service_note'] = _ai_service_health_cached['note']
        
        if _ai_service_health_cached['status'] != 'healthy':
            health_status['status'] = 'degraded'
        
        # Determine HTTP status code
        if health_status['status'] == 'healthy':
            status_code = 200
        elif health_status['status'] == 'degraded':
            status_code = 200  # Still operational
        else:
            status_code = 503  # Service unavailable
        
        return success_response(
            data=health_status,
            message=f"System status: {health_status['status']}",
            status_code=status_code
        )
