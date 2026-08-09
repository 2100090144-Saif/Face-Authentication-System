#!/usr/bin/env python
"""Test face matching logic."""
import sys
sys.path.insert(0, '/app')

from backend.app import db
from backend.models import User, FaceEncoding
from backend.services.face_service import get_face_service
from run import app
import numpy as np

with app.app_context():
    print("=" * 70)
    print("FACE MATCHING TEST")
    print("=" * 70)
    
    # Get face service
    face_service = get_face_service()
    
    # Get all active encodings
    active_encodings = FaceEncoding.query.filter_by(is_active=True).all()
    print(f"\n📸 Active Encodings in Database: {len(active_encodings)}")
    for enc in active_encodings:
        user = User.query.get(enc.user_id)
        print(f"  - ID={enc.id}, User={user.username} (ID={user.id}), Dims={len(enc.encoding)}")
    
    # Test: Compare each encoding against itself
    print(f"\n🧪 TEST 1: Self-Comparison (should have high confidence)")
    for enc in active_encodings:
        user = User.query.get(enc.user_id)
        is_match, confidence = face_service.recognizer.compare_faces(enc.encoding, enc.encoding)
        print(f"  - {user.username}: is_match={is_match}, confidence={confidence:.4f}")
    
    # Test: Compare encodings from same user
    print(f"\n🧪 TEST 2: Same User Comparison")
    user_4_encodings = FaceEncoding.query.filter_by(user_id=4, is_active=True).all()
    if len(user_4_encodings) >= 2:
        enc1 = user_4_encodings[0]
        enc2 = user_4_encodings[1]
        is_match, confidence = face_service.recognizer.compare_faces(enc1.encoding, enc2.encoding)
        print(f"  - Saif4u_1 encoding 1 vs 2: is_match={is_match}, confidence={confidence:.4f}")
    
    # Test: find_best_match with all encodings
    print(f"\n🧪 TEST 3: find_best_match with all encodings")
    known_encodings = [enc.encoding for enc in active_encodings]
    user_ids = [enc.user_id for enc in active_encodings]
    
    # Use first encoding as test
    test_encoding = active_encodings[0].encoding
    test_user = User.query.get(active_encodings[0].user_id)
    
    match_idx, confidence = face_service.recognizer.find_best_match(known_encodings, test_encoding)
    print(f"  - Test encoding from {test_user.username}")
    print(f"    Result: match_idx={match_idx}, confidence={confidence:.4f}")
    if match_idx is not None:
        matched_user_id = user_ids[match_idx]
        matched_user = User.query.get(matched_user_id)
        print(f"    Matched to: {matched_user.username} (ID={matched_user_id})")
    
    # Test: Check if encoding is numpy array
    print(f"\n🧪 TEST 4: Encoding Type Check")
    for enc in active_encodings:
        user = User.query.get(enc.user_id)
        print(f"  - {user.username}: type={type(enc.encoding)}, shape={np.array(enc.encoding).shape if hasattr(enc.encoding, '__len__') else 'N/A'}")

print("\n" + "=" * 70)
