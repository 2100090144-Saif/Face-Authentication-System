"""Settings routes."""
from flask import Blueprint
from backend.controllers import SettingsController

settings_bp = Blueprint('settings', __name__)

# GET /api/v1/settings
settings_bp.route('/', methods=['GET'])(SettingsController.get_settings)

# PUT /api/v1/settings/face-recognition
settings_bp.route('/face-recognition', methods=['PUT'])(SettingsController.update_face_recognition)
