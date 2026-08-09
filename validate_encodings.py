#!/usr/bin/env python3
"""
Encoding validation script.

Checks if face encodings can be loaded correctly from the database.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_encodings():
    """Validate that face encodings can be loaded from database."""
    try:
        from backend.app import create_app, db
        from backend.models import FaceEncoding, User
        
        app = create_app()
        
        with app.app_context():
            logger.info("=" * 60)
            logger.info("FACE ENCODING VALIDATION")
            logger.info("=" * 60)
            
            # Get all active encodings
            try:
                all_encodings = FaceEncoding.query.filter_by(is_active=True).all()
                logger.info(f"Found {len(all_encodings)} active face encodings in database")
            except Exception as e:
                logger.error(f"❌ Failed to query face encodings: {e}")
                return False
            
            if len(all_encodings) == 0:
                logger.info("✅ No face encodings to validate")
                return True
            
            # Try to load each encoding
            valid_count = 0
            invalid_count = 0
            invalid_ids = []
            
            for enc in all_encodings:
                try:
                    encoding_array = enc.encoding  # Uses property getter
                    if encoding_array is not None and len(encoding_array) == 128:
                        valid_count += 1
                    else:
                        invalid_count += 1
                        invalid_ids.append(enc.id)
                        logger.warning(f"⚠️  Encoding {enc.id} (user {enc.user_id}): Invalid or None")
                except Exception as e:
                    invalid_count += 1
                    invalid_ids.append(enc.id)
                    logger.error(f"❌ Encoding {enc.id} (user {enc.user_id}): Load error: {e}")
            
            logger.info("=" * 60)
            logger.info(f"VALIDATION RESULTS")
            logger.info("=" * 60)
            logger.info(f"Total encodings: {len(all_encodings)}")
            logger.info(f"Valid encodings: {valid_count}")
            logger.info(f"Invalid encodings: {invalid_count}")
            
            if invalid_count > 0:
                logger.warning("")
                logger.warning(f"⚠️  {invalid_count} encodings failed validation!")
                logger.warning(f"Invalid encoding IDs: {invalid_ids}")
                logger.warning("")
                logger.warning("RECOMMENDED ACTION:")
                logger.warning("1. Run: python migrate_encodings.py")
                logger.warning("2. Users should re-register their faces")
                logger.warning("")
                return False
            else:
                logger.info("✅ All encodings validated successfully!")
                return True
            
    except Exception as e:
        logger.error(f"❌ Validation failed: {e}", exc_info=True)
        return False

def main():
    """Main validation function."""
    success = validate_encodings()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
