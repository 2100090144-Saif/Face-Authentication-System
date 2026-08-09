"""Fix face encodings - delete all and force re-registration."""
import sys
sys.path.insert(0, '/app')

from backend.app import db
from backend.models import FaceEncoding
from run import app

with app.app_context():
    # Get all encodings
    encodings = FaceEncoding.query.all()
    print(f"Found {len(encodings)} face encodings:")
    
    for enc in encodings:
        print(f"  ID={enc.id}, user_id={enc.user_id}, dims={len(enc.encoding)}, active={enc.is_active}")
    
    # Delete all encodings
    if encodings:
        print("\nDeleting all face encodings...")
        for enc in encodings:
            db.session.delete(enc)
        db.session.commit()
        print(f"✅ Deleted {len(encodings)} face encodings")
        print("\n⚠️  All users must re-register their faces!")
    else:
        print("\nNo encodings to delete.")
