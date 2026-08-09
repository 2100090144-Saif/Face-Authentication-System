"""Routes package."""
from flask import Blueprint
from .auth_routes import auth_bp, auth_routes
from .face_routes import face_bp
from .settings_routes import settings_bp
from .frontend_routes import frontend_bp
from .health_routes import health_bp


def register_blueprints(app):
    """Register all blueprints with the app."""
    # API routes
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(face_bp, url_prefix='/api/v1/face')
    app.register_blueprint(settings_bp, url_prefix='/api/v1/settings')
    
    # Health check routes (no prefix - accessible at /health and /api/v1/health)
    app.register_blueprint(health_bp)
    
    # Frontend routes
    app.register_blueprint(frontend_bp)
    
    # Password reset routes (frontend pages)
    app.register_blueprint(auth_routes, url_prefix='/auth')


__all__ = ['register_blueprints']
