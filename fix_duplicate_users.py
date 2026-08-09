#!/usr/bin/env python
"""Fix duplicate user accounts."""
import sys
sys.path.insert(0, '/app')

from backend.app import db
from backend.models import User, FaceEncoding
from run import app

with app.app_context():
    print("=" * 70)
    print("FIXING DUPLICATE USER ACCOUNTS")
    print("=" * 70)
    
    # Find duplicate usernames (case-insensitive)
    users = User.query.all()
    username_map = {}
    
    for user in users:
        username_lower = user.username.lower()
        if username_lower not in username_map:
            username_map[username_lower] = []
        username_map[username_lower].append(user)
    
    # Find duplicates
    duplicates = {k: v for k, v in username_map.items() if len(v) > 1}
    
    if not duplicates:
        print("✅ No duplicate usernames found!")
    else:
        print(f"\n❌ Found {len(duplicates)} duplicate username(s):")
        for username_lower, users_list in duplicates.items():
            print(f"\n  Duplicate: '{username_lower}'")
            for user in users_list:
                encodings = FaceEncoding.query.filter_by(user_id=user.id).all()
                print(f"    - ID={user.id}, Username='{user.username}', Face Enabled={user.face_recognition_enabled}, Encodings={len(encodings)}")
            
            # Keep the one with encodings, delete the other
            user_with_encodings = None
            user_without_encodings = None
            
            for user in users_list:
                encodings = FaceEncoding.query.filter_by(user_id=user.id).all()
                if encodings:
                    user_with_encodings = user
                else:
                    user_without_encodings = user
            
            if user_with_encodings and user_without_encodings:
                print(f"\n    🔧 ACTION: Deleting user ID={user_without_encodings.id} (no encodings)")
                print(f"              Keeping user ID={user_with_encodings.id} (has {len(FaceEncoding.query.filter_by(user_id=user_with_encodings.id).all())} encodings)")
                
                # Delete the user without encodings
                db.session.delete(user_without_encodings)
                db.session.commit()
                print(f"    ✅ Deleted!")
    
    print("\n" + "=" * 70)
    print("FINAL STATE:")
    print("=" * 70)
    
    users = User.query.all()
    print(f"\n📋 Users ({len(users)} total):")
    for user in users:
        encodings = FaceEncoding.query.filter_by(user_id=user.id, is_active=True).all()
        print(f"  - ID={user.id}, Username={user.username}, Face Enabled={user.face_recognition_enabled}, Active Encodings={len(encodings)}")
    
    print("\n" + "=" * 70)
