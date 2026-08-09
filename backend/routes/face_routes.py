"""Face recognition routes."""
from flask import Blueprint
from backend.controllers import FaceController

face_bp = Blueprint('face', __name__)

# POST /api/v1/face/register
face_bp.route('/register', methods=['POST'])(FaceController.register_face)

# POST /api/v1/face/login
face_bp.route('/login', methods=['POST'])(FaceController.login_face)

# GET /api/v1/face/encodings
face_bp.route('/encodings', methods=['GET'])(FaceController.get_encodings)

# DELETE /api/v1/face/encodings
face_bp.route('/encodings', methods=['DELETE'])(FaceController.delete_encodings)
