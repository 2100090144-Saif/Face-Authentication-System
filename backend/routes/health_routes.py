"""Health check endpoints."""
from flask import Blueprint
from backend.controllers.health_controller import HealthController

health_bp = Blueprint('health', __name__)

# GET /health
health_bp.route('/health', methods=['GET'])(HealthController.health_check)

# GET /api/v1/health
health_bp.route('/api/v1/health', methods=['GET'])(HealthController.health_check)
