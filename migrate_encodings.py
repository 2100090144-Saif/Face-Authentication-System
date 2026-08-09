#!/usr/bin/env python3
"""
Migration script to fix face encoding storage format.

This script:
1. Backs up the current database
2. Drops the face_encodings table
3. Recreates it with the new JSON-based schema
4. Resets face_recognition_enabled for all users

Users will need to re-register their faces after this migration.
"""

import os
import sys
import shutil
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def backup_database():
    """Create a backup of the current database."""
    db_path = 'instance/app.db'
    
    if not os.path.exists(db_path):
        logger.warning(f"Database file not found: {db_path}")
        return None
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'instance/app.db.backup_{timestamp}'
    
    try:
        shutil.copy2(db_path, backup_path)
        logger.info(f"✅ Database backed up to: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"❌ Failed to backup database: {e}")
        return None

def migrate_database():
    """Migrate the database schema."""
    try:
        # Import Flask app and database
        from backend.app import create_app, db
        from backend.models import User, FaceEncoding
        
        app = create_app()
        
        with app.app_context():
            logger.info("Starting database migration...")
            
            # Get count of existing encodings
            try:
                encoding_count = FaceEncoding.query.count()
                user_count = User.query.filter_by(face_recognition_enabled=True).count()
                logger.info(f"Found {encoding_count} face encodings for {user_count} users")
            except Exception as e:
                logger.warning(f"Could not query existing data: {e}")
                encoding_count = 0
                user_count = 0
            
            # Drop and recreate face_encodings table
            logger.info("Dropping face_encodings table...")
            FaceEncoding.__table__.drop(db.engine, checkfirst=True)
            
            logger.info("Creating new face_encodings table with JSON schema...")
            FaceEncoding.__table__.create(db.engine, checkfirst=True)
            
            # Reset face_recognition_enabled for all users
            logger.info("Resetting face_recognition_enabled for all users...")
            User.query.update({User.face_recognition_enabled: False})
            db.session.commit()
            
            logger.info("✅ Migration completed successfully!")
            logger.info("")
            logger.info("=" * 60)
            logger.info("IMPORTANT: All users must re-register their faces")
            logger.info(f"- {user_count} users had face recognition enabled")
            logger.info(f"- {encoding_count} face encodings were cleared")
            logger.info("=" * 60)
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}", exc_info=True)
        return False

def main():
    """Main migration function."""
    logger.info("=" * 60)
    logger.info("Face Encoding Storage Format Migration")
    logger.info("=" * 60)
    logger.info("")
    logger.info("This migration will:")
    logger.info("1. Backup the current database")
    logger.info("2. Drop the face_encodings table")
    logger.info("3. Recreate it with JSON-based storage")
    logger.info("4. Reset face_recognition_enabled for all users")
    logger.info("")
    logger.info("⚠️  WARNING: All face encodings will be deleted!")
    logger.info("⚠️  Users will need to re-register their faces!")
    logger.info("")
    
    # Confirm migration
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    if response != 'yes':
        logger.info("Migration cancelled by user")
        return
    
    logger.info("")
    
    # Step 1: Backup database
    logger.info("Step 1: Backing up database...")
    backup_path = backup_database()
    if backup_path:
        logger.info(f"Backup created: {backup_path}")
    else:
        logger.warning("No backup created (database may not exist yet)")
    
    logger.info("")
    
    # Step 2: Migrate database
    logger.info("Step 2: Migrating database schema...")
    success = migrate_database()
    
    logger.info("")
    
    if success:
        logger.info("✅ Migration completed successfully!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Restart the application")
        logger.info("2. Users should re-register their faces")
        logger.info("3. Test face authentication")
        sys.exit(0)
    else:
        logger.error("❌ Migration failed!")
        if backup_path:
            logger.info(f"You can restore from backup: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
