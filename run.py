"""Main application entry point with dependency validation."""
import os
import sys
import logging
from dotenv import load_dotenv

# Load .env before anything else
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Validate dependencies before starting the app
logger.info("Running dependency validation...")
try:
    from validate_dependencies import main as validate_deps
    if not validate_deps():
        logger.error("Dependency validation failed. Please check the logs above.")
        sys.exit(1)
except Exception as e:
    logger.warning(f"Could not run dependency validation: {e}")
    logger.warning("Proceeding with application startup...")

from backend.app import create_app

# Validate face encodings after app is created
logger.info("Validating face encodings...")
try:
    from validate_encodings import validate_encodings
    app_temp = create_app(os.environ.get('FLASK_ENV', 'development'))
    with app_temp.app_context():
        if not validate_encodings():
            logger.warning("⚠️  Face encoding validation failed!")
            logger.warning("⚠️  Some users may need to re-register their faces")
            logger.warning("⚠️  Run 'python migrate_encodings.py' to fix corrupted data")
        else:
            logger.info("✅ Face encoding validation passed")
except Exception as e:
    logger.warning(f"Could not validate face encodings: {e}")
    logger.warning("Proceeding with application startup...")

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    use_https = os.environ.get('FLASK_HTTPS', 'true').lower() == 'true'

    scheme = 'https' if use_https else 'http'
    ssl_context = 'adhoc' if use_https else None

    print(f"\n{'='*50}")
    print(f"  Face Authentication System")
    print(f"  URL: {scheme}://{host}:{port}")
    if use_https:
        print(f"  NOTE: Accept browser SSL warning once")
    print(f"{'='*50}\n")

    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG'],
        ssl_context=ssl_context
    )
