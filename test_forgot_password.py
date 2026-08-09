#!/usr/bin/env python
"""
Quick test script for forgot password feature.
Tests the API endpoints without sending actual emails.
"""
import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed certificate
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

BASE_URL = "https://localhost:5000"

def test_forgot_password_api():
    """Test the forgot password API endpoint."""
    print("🧪 Testing Forgot Password Feature\n")
    print("=" * 60)
    
    # Test 1: Request password reset
    print("\n1️⃣ Testing password reset request...")
    print("-" * 60)
    
    test_email = "test@example.com"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/forgot-password",
            json={"email": test_email},
            verify=False,
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Password reset request endpoint working!")
        else:
            print("⚠️  Unexpected status code")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Run: docker-compose up -d")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 2: Test with invalid token (should fail)
    print("\n2️⃣ Testing password reset with invalid token...")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/reset-password",
            json={
                "token": "invalid-token-12345",
                "new_password": "NewPassword123!"
            },
            verify=False,
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✅ Invalid token correctly rejected!")
        else:
            print("⚠️  Unexpected status code")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    # Test 3: Check frontend pages exist
    print("\n3️⃣ Testing frontend pages...")
    print("-" * 60)
    
    pages = [
        ("/auth/forgot-password", "Forgot Password Form"),
        ("/auth/reset-password/test-token", "Reset Password Form")
    ]
    
    for path, name in pages:
        try:
            response = requests.get(
                f"{BASE_URL}{path}",
                verify=False,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ {name}: Available")
            else:
                print(f"⚠️  {name}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 FORGOT PASSWORD FEATURE TEST COMPLETE!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("1. Configure email settings in .env file")
    print("2. Test with real email address")
    print("3. Check email inbox for reset link")
    print("\n💡 To configure email:")
    print("   Edit .env file and add:")
    print("   MAIL_SERVER=smtp.gmail.com")
    print("   MAIL_USERNAME=your-email@gmail.com")
    print("   MAIL_PASSWORD=your-app-password")
    print("\n🔗 Access the feature:")
    print(f"   {BASE_URL}/login")
    print("   Click 'Forgot Password?' link")
    
    return True

if __name__ == "__main__":
    test_forgot_password_api()
