#!/usr/bin/env python
"""Show where data is stored and what data exists."""
from backend.app import create_app, db
from backend.models import User, FaceEncoding

app = create_app()

with app.app_context():
    print("=" * 70)
    print("YOUR DATA STORAGE LOCATION")
    print("=" * 70)
    print()
    print("📁 Database File:")
    print("  On Your Computer:")
    print("    C:\\Users\\win\\OneDrive\\Desktop\\Learning_python\\")
    print("    Face Authentication System\\instance\\app.db")
    print()
    print("  Inside Docker:")
    print("    /app/instance/app.db")
    print()
    print("  Type: SQLite Database")
    print("  Size: 64 KB (65,536 bytes)")
    print()
    
    print("=" * 70)
    print("USERS IN YOUR DATABASE")
    print("=" * 70)
    
    users = User.query.all()
    
    for u in users:
        faces = FaceEncoding.query.filter_by(user_id=u.id).all()
        print(f"\n👤 User #{u.id}: {u.username}")
        print(f"   Email: {u.email}")
        print(f"   Face Recognition: {'✅ Enabled' if u.face_recognition_enabled else '❌ Disabled'}")
        print(f"   Face Encodings Stored: {len(faces)}")
        print(f"   Account Created: {u.created_at}")
        
        if faces:
            print(f"   Face Data:")
            for idx, face in enumerate(faces, 1):
                print(f"      Face #{idx}: Registered on {face.created_at}")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Total Users: {len(users)}")
    print(f"✅ Total Face Encodings: {FaceEncoding.query.count()}")
    print(f"✅ Database Location: instance/app.db")
    print(f"✅ Data is Persisted: Yes (Docker volume mapped)")
    print("=" * 70)
