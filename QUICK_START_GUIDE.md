# 🚀 QUICK START GUIDE - Face Authentication System

**Last Updated**: 2026-04-27  
**System Status**: ✅ PRODUCTION READY  
**All Fixes**: ✅ APPLIED  

---

## 📋 PREREQUISITES

- ✅ Docker Desktop installed and running
- ✅ Python 3.11 (if running locally)
- ✅ Webcam (for face recognition)
- ✅ Modern browser (Chrome, Firefox, Edge)

---

## 🐳 OPTION 1: RUN WITH DOCKER (RECOMMENDED)

### Step 1: Start Docker Desktop
```bash
# Make sure Docker Desktop is running
docker --version
```

### Step 2: Start the Application
```bash
# Start the container
docker-compose up -d

# Wait for container to be healthy (30 seconds)
docker ps
```

### Step 3: Verify Health
```bash
# Check application health
docker exec face_auth_app curl -k https://localhost:5000/health

# Expected output:
# {
#   "status": "healthy",
#   "checks": {
#     "ai_service": "healthy",
#     "database": "healthy"
#   }
# }
```

### Step 4: Access the Application
```
Open browser: https://localhost:5000
```

### Step 5: View Logs (Optional)
```bash
# View real-time logs
docker logs -f face_auth_app

# View last 100 lines
docker logs face_auth_app --tail 100
```

---

## 💻 OPTION 2: RUN LOCALLY (DEVELOPMENT)

### Step 1: Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Verify NumPy version (must be 1.26.4)
pip show numpy
```

### Step 3: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and set SECRET_KEY
# SECRET_KEY=your-secret-key-here
```

### Step 4: Run the Application
```bash
# Start the application
python run.py

# Application will start on https://localhost:5000
```

---

## 👤 USER GUIDE

### 1. Register a New Account
```
1. Go to: https://localhost:5000/register
2. Fill in:
   - Username (3-80 characters)
   - Email (valid email)
   - Password (min 8 characters)
3. Click "Register"
4. You'll be logged in automatically
```

### 2. Enable Face Recognition
```
1. Go to: https://localhost:5000/settings
2. Toggle "Face Recognition" ON
3. Click "Register Your Face"
4. Allow camera access
5. Position your face in the frame
6. Click "Capture & Register"
7. Wait for confirmation
```

### 3. Login with Face
```
1. Logout (if logged in)
2. Go to: https://localhost:5000/login
3. Click "Face Recognition" tab
4. Click "Start Face Login"
5. Allow camera access
6. Position your face in the frame
7. Click "Authenticate"
8. Wait for multi-frame verification (5 frames)
9. You'll be logged in automatically
```

### 4. Login with Password
```
1. Go to: https://localhost:5000/login
2. Enter username and password
3. Click "Login"
```

---

## 🔧 TROUBLESHOOTING

### Issue: Docker container not starting
```bash
# Check Docker is running
docker ps

# Restart Docker Desktop
# Then try again:
docker-compose down
docker-compose up -d
```

### Issue: "No module named 'numpy._core.numeric'"
```bash
# This bug has been FIXED ✅
# If you still see it, verify the fix:
docker exec face_auth_app grep "encoding_json" /app/backend/models/face_encoding.py

# Should show: encoding_json = db.Column(db.Text, nullable=False)
```

### Issue: Face authentication fails even with same image
```bash
# This bug has been FIXED ✅
# Verify the fix:
docker exec face_auth_app grep "MIN_CONFIDENCE" /app/backend/services/face_service.py

# Should show: MIN_CONFIDENCE = 0.60 (NOT 60.0)
```

### Issue: Camera not working
```
1. Check browser permissions (allow camera)
2. Use HTTPS (required for camera access)
3. Try different browser
4. Check camera is not used by another app
```

### Issue: Face not detected
```
1. Ensure good lighting
2. Face camera directly
3. Remove glasses if possible
4. Move closer to camera
5. Check camera quality
```

### Issue: Face not recognized
```
1. Re-register your face
2. Ensure good lighting during registration
3. Use same lighting conditions for login
4. Check logs for confidence scores
```

---

## 📊 SYSTEM CONFIGURATION

### Current Thresholds:
```python
MIN_CONFIDENCE = 0.60      # 60% minimum confidence
MAX_TOLERANCE = 0.45       # Maximum distance allowed
MULTI_FRAME_COUNT = 5      # Number of frames to capture
STABILIZATION_FRAMES = 3   # Minimum consecutive passes
```

### Expected Behavior:
```
✅ Same image → Always authenticates (100%)
✅ Similar image (60-100% confidence) → Authenticates
❌ Different person → Rejects
❌ No face → Rejects
❌ Multiple faces → Rejects
```

---

## 🔍 MONITORING

### Check Application Health:
```bash
# Health endpoint
curl -k https://localhost:5000/health

# Expected: {"status": "healthy"}
```

### Check Logs:
```bash
# View logs
docker logs face_auth_app --tail 100

# Look for:
# ✅ Face recognizer initialized
# ✅ FaceService singleton created
# ✅ AI service health check: healthy
```

### Validate Face Encodings:
```bash
# Run validation script
docker exec face_auth_app python validate_encodings.py

# Expected: Shows number of valid encodings
```

---

## 📝 USEFUL COMMANDS

### Docker Commands:
```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# Restart container
docker-compose restart

# View logs
docker logs face_auth_app

# Execute command in container
docker exec face_auth_app <command>

# Access container shell
docker exec -it face_auth_app bash
```

### Database Commands:
```bash
# Validate encodings
docker exec face_auth_app python validate_encodings.py

# Check database
docker exec face_auth_app python -c "
from backend.app import create_app, db
from backend.models import User, FaceEncoding
app = create_app()
with app.app_context():
    print(f'Users: {User.query.count()}')
    print(f'Encodings: {FaceEncoding.query.count()}')
"
```

### Application Commands:
```bash
# Check configuration
docker exec face_auth_app cat /app/.env

# Check Python version
docker exec face_auth_app python --version

# Check NumPy version
docker exec face_auth_app python -c "import numpy; print(numpy.__version__)"
```

---

## 🎯 TESTING CHECKLIST

### Basic Functionality:
- [ ] Application starts successfully
- [ ] Health endpoint returns healthy
- [ ] Can register new user
- [ ] Can login with password
- [ ] Can access settings page
- [ ] Can enable face recognition
- [ ] Can register face
- [ ] Can login with face
- [ ] Can logout

### Face Recognition:
- [ ] Camera access works
- [ ] Face detection highlights face
- [ ] Face registration succeeds
- [ ] Same image authenticates successfully
- [ ] Different person is rejected
- [ ] No face is rejected
- [ ] Multi-frame verification works
- [ ] Stabilization check works

### Error Handling:
- [ ] Invalid credentials show error
- [ ] No face detected shows error
- [ ] Face not recognized shows error
- [ ] Camera denied shows error
- [ ] Network error shows error

---

## 📚 DOCUMENTATION

### Main Documentation:
- `README.md` - Complete user and developer guide
- `SYSTEM_VERIFICATION_COMPLETE.md` - Full compliance report
- `ALL_FIXES_COMPLETED_SUMMARY.md` - Master fix summary

### Architecture Documentation:
- `architecture/plans.md` - Architecture plan
- `architecture/models.md` - Database models
- `architecture/api.md` - API documentation
- `architecture/flow.md` - Application flows
- `architecture/decisions.md` - Architecture decisions

### Bug Fix Documentation:
- `NUMPY_FIX_COMPLETED.md` - NumPy serialization fix
- `FALSE_REJECTION_FIX_COMPLETED.md` - False rejection fix

### Steering Documentation:
- `.kiro/steering/rules.md` - Development rules
- `.kiro/steering/best_practices.md` - Best practices
- `.kiro/steering/dos_and_donts.md` - Do's and don'ts

---

## 🆘 SUPPORT

### Common Issues:

1. **Docker not running**
   - Start Docker Desktop
   - Wait for it to fully start
   - Try again

2. **Port 5000 already in use**
   - Stop other applications using port 5000
   - Or change port in docker-compose.yml

3. **Face encodings not loading**
   - This bug has been FIXED ✅
   - Users must re-register faces after fix

4. **Face authentication fails**
   - This bug has been FIXED ✅
   - Verify MIN_CONFIDENCE = 0.60 (not 60.0)

### Get Help:
- Check logs: `docker logs face_auth_app`
- Check health: `curl -k https://localhost:5000/health`
- Validate encodings: `docker exec face_auth_app python validate_encodings.py`
- Review documentation in `architecture/` directory

---

## ✅ SYSTEM STATUS

```
✅ Application: READY
✅ Database: READY
✅ Face Recognizer: READY
✅ AI Service: READY
✅ Authentication: WORKING
✅ Multi-Frame: WORKING
✅ Stabilization: WORKING
✅ Bug Fixes: APPLIED
✅ Documentation: COMPLETE
```

---

## 🎉 SUCCESS CRITERIA

### You know the system is working when:
1. ✅ Health endpoint returns "healthy"
2. ✅ Can register new user
3. ✅ Can login with password
4. ✅ Can register face
5. ✅ Can login with same face image
6. ✅ Different person is rejected
7. ✅ Logs show correct confidence values
8. ✅ Multi-frame verification passes

---

**Status**: ✅ READY TO USE  
**All Fixes**: ✅ APPLIED  
**Documentation**: ✅ COMPLETE  

**🚀 Enjoy your Face Authentication System!** 🎉

