#!/usr/bin/env python
"""
Migration script to add password reset fields to User model.
Run this script to update existing database.
"""
from backend.app import create_app, db
from backend.models import User

def migrate():
    """Add password reset fields to users table."""
    app = create_app()
    
    with app.app_context():
        print("🔄 Starting database migration...")
        print("Adding password reset fields to users table...")
        
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'reset_token' in columns and 'reset_token_expiry' in columns:
                print("✅ Password reset fields already exist!")
                return
            
            # Add columns using raw SQL
            with db.engine.connect() as conn:
                if 'reset_token' not in columns:
                    conn.execute(db.text(
                        "ALTER TABLE users ADD COLUMN reset_token VARCHAR(100)"
                    ))
                    conn.execute(db.text(
                        "CREATE INDEX ix_users_reset_token ON users (reset_token)"
                    ))
                    print("✅ Added reset_token column")
                
                if 'reset_token_expiry' not in columns:
                    conn.execute(db.text(
                        "ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME"
                    ))
                    print("✅ Added reset_token_expiry column")
                
                conn.commit()
            
            print("✅ Migration completed successfully!")
            print("\n📊 Database schema updated:")
            print("  - reset_token (VARCHAR(100), indexed)")
            print("  - reset_token_expiry (DATETIME)")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            print("\nℹ️  If you're starting fresh, just run:")
            print("   python run.py")
            print("   (Database will be created automatically)")
            raise

if __name__ == '__main__':
    migrate()
