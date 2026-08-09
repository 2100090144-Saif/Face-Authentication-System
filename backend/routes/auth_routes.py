"""Authentication routes."""
from flask import Blueprint
from backend.controllers import AuthController
from backend.controllers.password_reset_controller import PasswordResetController

auth_bp = Blueprint('auth', __name__)

# POST /api/v1/auth/register
auth_bp.route('/register', methods=['POST'])(AuthController.register)

# POST /api/v1/auth/login
auth_bp.route('/login', methods=['POST'])(AuthController.login)

# POST /api/v1/auth/logout
auth_bp.route('/logout', methods=['POST'])(AuthController.logout)

# GET /api/v1/auth/me
auth_bp.route('/me', methods=['GET'])(AuthController.get_current_user)

# POST /api/v1/auth/forgot-password
auth_bp.route('/forgot-password', methods=['POST'])(PasswordResetController.request_reset)

# Password reset routes (for frontend pages)
auth_routes = Blueprint('auth_routes', __name__)

# GET /auth/forgot-password
auth_routes.route('/forgot-password', methods=['GET'])(PasswordResetController.show_forgot_password_form)

# GET /auth/reset-password/<token>
auth_routes.route('/reset-password/<token>', methods=['GET'])(PasswordResetController.verify_reset_token)

# POST /auth/reset-password/<token>
auth_routes.route('/reset-password/<token>', methods=['POST'])(PasswordResetController.reset_password)
