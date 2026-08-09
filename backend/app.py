"""Flask application factory and extensions."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_name='development'):
    """Create and configure Flask application."""
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Load configuration
    from backend.config import get_config
    app.config.from_object(get_config())
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Setup logging
    from backend.config.logging_config import setup_logging
    setup_logging(app)
    
    # Register error handlers
    from backend.middleware.error_handler import register_error_handlers
    register_error_handlers(app)
    
    # Configure login manager
    login_manager.login_view = 'frontend.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # User loader for Flask-Login
    from backend.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from backend.routes import register_blueprints
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
