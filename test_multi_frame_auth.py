#!/usr/bin/env python3
"""
Test multi-frame face authentication to verify stability and consistency.
"""
import sys
import os
import time
import numpy as np
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app, db
from backend.models import User, FaceEncoding
from backend.services.face_service import get_face_service
from ai_service.utils import load_image_from_bytes

def test_multi_frame_authentication():
    """Test multi-frame authentication with existing user images."""
    app = create_app()
    
    with app.app_context():
        print("🧪 Multi-Frame Face Authentication Test")
        print("=" * 50)
        
        # Get face service
        face_service = get_face_service()
        
        # Get all users with face recognition enabled
        users_with_faces = User.query.filter_by(face_recognition_enabled=True).all()
        
        if not users_with_faces:
            print("❌ No users with face recognition enabled found")
            return
        
        print(f"👥 Found {len(users_with_faces)} users with face recognition enabled")
        
        # Test with existing user images
        test_images = [
            "ai_service/data/user_1776251199.jpg",
            "ai_service/data/user_1776338267.jpg", 
            "ai_service/data/user_1776338361.jpg",
            "ai_service/data/user_1776665716.jpg",
            "ai_service/data/user_1776672716.jpg"
        ]
        
        available_images = []
        for img_path in test_images:
            if os.path.exists(img_path):
                available_images.append(img_path)
        
        if not available_images:
            print("❌ No test images found")
            return
        
        print(f"🖼️  Found {len(available_images)} test images")
        
        # Test each image multiple times to check consistency
        for img_path in available_images:
            print(f"\n📸 Testing image: {os.path.basename(img_path)}")
            print("-" * 40)
            
            try:
                # Load image
                with open(img_path, 'rb') as f:
                    image_bytes = f.read()
                
                # Test multiple times
                results = []
                for test_num in range(3):
                    print(f"  Test {test_num + 1}/3: ", end="", flush=True)
                    
                    start_time = time.time()
                    user, confidence, error = face_service.authenticate_face(image_bytes)
                    end_time = time.time()
                    
                    duration = end_time - start_time
                    
                    result = {
                        'test_num': test_num + 1,
                        'user': user,
                        'confidence': confidence,
                        'error': error,
                        'duration': duration
                    }
                    results.append(result)
                    
                    if error:
                        print(f"❌ FAILED - {error}")
                    elif user:
                        print(f"✅ SUCCESS - {user.username} ({confidence:.2%}) [{duration:.2f}s]")
                    else:
                        print(f"❌ FAILED - No user returned")
                    
                    # Small delay between tests
                    time.sleep(0.5)
                
                # Analyze results
                print(f"\n  📊 Analysis:")
                
                successful_results = [r for r in results if r['user'] is not None and r['error'] is None]
                
                if successful_results:
                    confidences = [r['confidence'] for r in successful_results]
                    durations = [r['duration'] for r in successful_results]
                    
                    avg_confidence = sum(confidences) / len(confidences)
                    min_confidence = min(confidences)
                    max_confidence = max(confidences)
                    confidence_std = np.std(confidences)
                    
                    avg_duration = sum(durations) / len(durations)
                    
                    print(f"    ✅ Success Rate: {len(successful_results)}/3 ({len(successful_results)/3*100:.1f}%)")
                    print(f"    📈 Confidence: {avg_confidence:.2%} (±{confidence_std:.2%})")
                    print(f"    📊 Range: {min_confidence:.2%} - {max_confidence:.2%}")
                    print(f"    ⏱️  Avg Duration: {avg_duration:.2f}s")
                    
                    # Check stability
                    if confidence_std < 0.05:  # Less than 5% standard deviation
                        print(f"    🎯 STABLE - Low confidence variation")
                    else:
                        print(f"    ⚠️  UNSTABLE - High confidence variation ({confidence_std:.2%})")
                    
                    # Check if all results are consistent
                    users = [r['user'].username for r in successful_results if r['user']]
                    if len(set(users)) == 1:
                        print(f"    👤 CONSISTENT - Same user: {users[0]}")
                    else:
                        print(f"    ❌ INCONSISTENT - Different users: {set(users)}")
                else:
                    print(f"    ❌ No successful authentications")
                    errors = [r['error'] for r in results if r['error']]
                    if errors:
                        print(f"    🚫 Errors: {set(errors)}")
                
            except Exception as e:
                print(f"❌ Error testing {img_path}: {e}")
        
        # Test with unknown face (should be rejected consistently)
        print(f"\n🚫 Testing Unknown Face Rejection")
        print("-" * 40)
        
        # Create a synthetic "unknown" image (noise)
        try:
            import cv2
            
            # Create random noise image
            noise_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # Add some face-like structure
            cv2.rectangle(noise_image, (200, 150), (440, 350), (128, 128, 128), -1)  # Face
            cv2.circle(noise_image, (280, 220), 20, (64, 64, 64), -1)  # Left eye
            cv2.circle(noise_image, (360, 220), 20, (64, 64, 64), -1)  # Right eye
            cv2.rectangle(noise_image, (310, 280), (330, 300), (64, 64, 64), -1)  # Nose
            cv2.rectangle(noise_image, (300, 320), (340, 340), (64, 64, 64), -1)  # Mouth
            
            # Convert to bytes
            _, buffer = cv2.imencode('.jpg', noise_image)
            noise_bytes = buffer.tobytes()
            
            # Test multiple times
            rejection_count = 0
            for test_num in range(3):
                print(f"  Unknown Test {test_num + 1}/3: ", end="", flush=True)
                
                user, confidence, error = face_service.authenticate_face(noise_bytes)
                
                if user is None:
                    print(f"✅ CORRECTLY REJECTED - {error or 'No match'}")
                    rejection_count += 1
                else:
                    print(f"❌ INCORRECTLY ACCEPTED - {user.username} ({confidence:.2%})")
            
            print(f"\n  📊 Unknown Face Analysis:")
            print(f"    🚫 Rejection Rate: {rejection_count}/3 ({rejection_count/3*100:.1f}%)")
            
            if rejection_count == 3:
                print(f"    ✅ PERFECT - All unknown faces rejected")
            elif rejection_count >= 2:
                print(f"    ⚠️  GOOD - Most unknown faces rejected")
            else:
                print(f"    ❌ POOR - Too many false positives")
                
        except Exception as e:
            print(f"❌ Error testing unknown face: {e}")
        
        print(f"\n🏁 Multi-Frame Authentication Test Complete")

if __name__ == "__main__":
    test_multi_frame_authentication()