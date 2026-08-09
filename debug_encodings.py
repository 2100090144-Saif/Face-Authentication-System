#!/usr/bin/env python
"""Debug face encodings in database."""
import sys
sys.path.insert(0, '/app')

from backend.app import db
from backend.models import User, FaceEncoding
from run import app

with app.app_context():
    print("=" * 70)
    print("FACE ENCODING DATABASE DEBUG")
    print("=" * 70)
    
    # Get all users
    users = User.query.all()
    print(f"\n📋 USERS ({len(users)} total):")
    for user in users:
        print(f"  - ID={user.id}, Username={user.username}, Face Enabled={user.face_recognition_enabled}")
    
    # Get all face encodings
    encodings = FaceEncoding.query.all()
    print(f"\n📸 FACE ENCODINGS ({len(encodings)} total):")
    for enc in encodings:
        user = User.query.get(enc.user_id)
        username = user.username if user else "❌ UNKNOWN"
        print(f"  - ID={enc.id}, User={username} (user_id={enc.user_id}), Active={enc.is_active}, Dims={len(enc.encoding)}")
    
    # Check active encodings
    print(f"\n🔍 ACTIVE ENCODINGS CHECK:")
    active_encodings = FaceEncoding.query.filter_by(is_active=True).all()
    print(f"  Total active: {len(active_encodings)}")
    
    if len(active_encodings) == 0:
        print("  ⚠️  WARNING: No active encodings found!")
    else:
        for enc in active_encodings:
            user = User.query.get(enc.user_id)
            print(f"    ✅ User {user.username}: dims={len(enc.encoding)}, type={type(enc.encoding).__name__}")
    
    # Check for issues
    print(f"\n⚠️  POTENTIAL ISSUES:")
    
    # Issue 1: Encodings without users
    orphaned = FaceEncoding.query.filter(~FaceEncoding.user_id.in_([u.id for u in users])).all()
    if orphaned:
        print(f"  ❌ Orphaned encodings (no user): {len(orphaned)}")
    else:
        print(f"  ✅ No orphaned encodings")
    
    # Issue 2: Users with face enabled but no encodings
    for user in users:
        if user.face_recognition_enabled:
            user_encodings = FaceEncoding.query.filter_by(user_id=user.id, is_active=True).all()
            if not user_encodings:
                print(f"  ❌ User {user.username} has face_recognition_enabled=True but NO active encodings!")
            else:
                print(f"  ✅ User {user.username} has {len(user_encodings)} active encoding(s)")
    
    # Issue 3: Encoding dimensions mismatch
    dims_set = set()
    for enc in active_encodings:
        dims_set.add(len(enc.encoding))
    
    if len(dims_set) > 1:
        print(f"  ❌ ENCODING DIMENSION MISMATCH: {dims_set}")
    else:
        print(f"  ✅ All encodings have consistent dimensions: {dims_set}")

print("\n" + "=" * 70)
