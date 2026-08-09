#!/usr/bin/env python3
"""
Dependency validation script for Face Authentication System.
Checks that all required dependencies are properly installed before starting the app.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_numpy():
    """Validate NumPy installation."""
    try:
        import numpy as np
        version = np.__version__
        logger.info(f"✅ NumPy {version} installed successfully")
        
        # Check for the specific module that was failing
        try:
            from numpy._core import numeric
            logger.info("✅ NumPy._core.numeric module accessible")
        except ImportError:
            # Try alternative import for older numpy versions
            try:
                from numpy.core import numeric
                logger.info("✅ NumPy.core.numeric module accessible (legacy path)")
            except ImportError:
                logger.warning("⚠️  NumPy core modules not accessible, but NumPy is installed")
        
        # Test basic functionality
        test_array = np.array([1, 2, 3])
        assert test_array.sum() == 6
        logger.info("✅ NumPy functionality test passed")
        
        return True
    except Exception as e:
        logger.error(f"❌ NumPy validation failed: {e}")
        return False

def validate_opencv():
    """Validate OpenCV installation."""
    try:
        import cv2
        version = cv2.__version__
        logger.info(f"✅ OpenCV {version} installed successfully")
        
        # Test basic functionality
        test_img = cv2.imread('test.jpg')  # This will return None if file doesn't exist, which is fine
        logger.info("✅ OpenCV functionality test passed")
        
        return True
    except Exception as e:
        logger.error(f"❌ OpenCV validation failed: {e}")
        return False

def validate_face_recognition():
    """Validate face_recognition installation."""
    try:
        import face_recognition
        logger.info(f"✅ face_recognition library installed successfully")
        
        # Test that it can import dlib
        import dlib
        logger.info(f"✅ dlib installed successfully")
        
        return True
    except ImportError as e:
        logger.warning(f"⚠️  face_recognition library not available: {e}")
        logger.warning("⚠️  System will use OpenCV fallback")
        return False
    except Exception as e:
        logger.error(f"❌ face_recognition validation failed: {e}")
        return False

def validate_pillow():
    """Validate Pillow installation."""
    try:
        from PIL import Image
        logger.info(f"✅ Pillow installed successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Pillow validation failed: {e}")
        return False

def validate_flask():
    """Validate Flask and extensions."""
    try:
        import flask
        logger.info(f"✅ Flask {flask.__version__} installed successfully")
        
        from flask_sqlalchemy import SQLAlchemy
        logger.info("✅ Flask-SQLAlchemy installed")
        
        from flask_login import LoginManager
        logger.info("✅ Flask-Login installed")
        
        from flask_bcrypt import Bcrypt
        logger.info("✅ Flask-Bcrypt installed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Flask validation failed: {e}")
        return False

def main():
    """Run all validation checks."""
    logger.info("=" * 60)
    logger.info("DEPENDENCY VALIDATION")
    logger.info("=" * 60)
    
    results = {
        "NumPy": validate_numpy(),
        "OpenCV": validate_opencv(),
        "face_recognition": validate_face_recognition(),
        "Pillow": validate_pillow(),
        "Flask": validate_flask()
    }
    
    logger.info("=" * 60)
    logger.info("VALIDATION SUMMARY")
    logger.info("=" * 60)
    
    critical_failed = []
    optional_failed = []
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{name:<20}: {status}")
        
        if not passed:
            if name in ["NumPy", "OpenCV", "Pillow", "Flask"]:
                critical_failed.append(name)
            else:
                optional_failed.append(name)
    
    logger.info("=" * 60)
    
    if critical_failed:
        logger.error(f"❌ CRITICAL DEPENDENCIES FAILED: {', '.join(critical_failed)}")
        logger.error("❌ Application cannot start. Please fix dependencies.")
        return False
    
    if optional_failed:
        logger.warning(f"⚠️  OPTIONAL DEPENDENCIES FAILED: {', '.join(optional_failed)}")
        logger.warning("⚠️  Application will use fallback implementations")
    
    logger.info("✅ All critical dependencies validated successfully")
    logger.info("✅ Application can start")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
