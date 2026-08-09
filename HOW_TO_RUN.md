# 🚀 How to Run Face Authentication System

## 📋 **Quick Start (3 Methods)**

### **Method 1: Docker Compose (RECOMMENDED ✅)**
```bash
# Start the application
docker-compose up

# Or run in background (detached mode)
docker-compose up -d
```

### **Method 2: Docker Only**
```bash
# Build the image
docker build -t face_auth_system:latest .

# Run the container
docker run -d -p 5000:5000 \
  -v ./instance:/app/instance \
  -v ./logs:/app/logs \
  -v ./ai_service/data:/app/ai_service/data \
  --name face_auth_app \
  face_auth_system:latest
```

### **Method 3: Python Directly (Without Docker)**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

---

## 🎯 **RECOMMENDED: Docker Compose Method**

### **Step 1: Start the Application**

```bash
# Navigate to project directory
cd "Face Authentication System"

# Start with logs visible
docker-compose up

# OR start in background
docker-compose up -d
```

**Expected Output:**
```
✔ Container face_auth_app Running
Attaching to face_auth_app
face_auth_app  | Face Authentication System
face_auth_app  | URL: https://0.0.0.0:5000
face_auth_app  | NOTE: Accept browser SSL warning once
```

### **Step 2: Access the Application**

Open your browser and go to:
```
https://localhost:5000
```

**Note**: You'll see a security warning because we're using a self-signed SSL certificate. Click "Advanced" → "Proceed to localhost" (this is safe for local development).

### **Step 3: Verify It's Running**

```bash
# Check container status
docker ps

# Check logs
docker logs face_auth_app

# Check health
curl -k https://localhost:5000/health
```

---

## 🛑 **How to Stop the Application**

### **If Running in Foreground:**
```bash
# Press Ctrl+C in the terminal
```

### **If Running in Background:**
```bash
# Stop the container
docker-compose down

# OR stop without removing
docker-compose stop
```

---

## 🔄 **Common Commands**

### **Restart the Application**
```bash
docker-compose restart
```

### **Rebuild After Code Changes**
```bash
# Rebuild and restart
docker-compose up --build

# OR rebuild image only
docker build -t face_auth_system:latest .
docker-compose up
```

### **View Logs**
```bash
# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker logs --tail 100 face_auth_app

# View specific service logs
docker-compose logs -f app
```

### **Check Status**
```bash
# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# Check Docker Compose status
docker-compose ps
```

---

## 🌐 **Accessing the Application**

### **URLs:**

| Service | URL | Description |
|---------|-----|-------------|
| **Main App** | https://localhost:5000 | Face authentication web interface |
| **Health Check** | https://localhost:5000/health | System health status |
| **Login** | https://localhost:5000/login | User login page |
| **Register** | https://localhost:5000/register | User registration |
| **Face Login** | https://localhost:5000/face-login | Face authentication |

### **Test the Application:**

1. **Register a User**
   - Go to: https://localhost:5000/register
   - Create an account with username/email/password

2. **Register Your Face**
   - Login with credentials
   - Go to Settings
   - Upload your face photo
   - Click "Register Face"

3. **Test Face Login**
   - Logout
   - Go to: https://localhost:5000/face-login
   - Upload your face photo
   - Should log you in automatically!

---

## 🔧 **Troubleshooting**

### **Problem 1: Port 5000 Already in Use**

**Error:**
```
Error: bind: address already in use
```

**Solution:**
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# OR change the port in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

### **Problem 2: Docker Not Running**

**Error:**
```
Cannot connect to the Docker daemon
```

**Solution:**
```bash
# Start Docker Desktop
# Wait for it to fully start
# Then try again
docker-compose up
```

### **Problem 3: Database Permission Error**

**Error:**
```
sqlite3.OperationalError: unable to open database file
```

**Solution:**
```bash
# Stop the application
docker-compose down

# Create instance directory
mkdir -p instance

# Restart
docker-compose up
```

### **Problem 4: Face Recognition Not Working**

**Check logs:**
```bash
docker logs face_auth_app | grep "face_recognition"
```

**Expected:**
```
✅ Face recognizer initialized with face_recognition library
```

**If you see "OpenCV fallback":**
- This is normal! The system will still work
- OpenCV fallback is automatic and functional

### **Problem 5: SSL Certificate Warning**

**This is NORMAL for local development!**

**Solution:**
- Click "Advanced" in browser
- Click "Proceed to localhost (unsafe)"
- This is safe for local development

**For production:**
- Use a real SSL certificate (Let's Encrypt)
- Or configure a reverse proxy (nginx)

---

## 📊 **Monitoring the Application**

### **Real-Time Logs**
```bash
# Follow all logs
docker-compose logs -f

# Follow only errors
docker logs face_auth_app 2>&1 | grep ERROR

# Follow authentication attempts
docker logs -f face_auth_app | grep "STEP=START"
```

### **Check System Health**
```bash
# Health endpoint
curl -k https://localhost:5000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-04-22T12:00:00"
}
```

### **Monitor Resource Usage**
```bash
# Container stats
docker stats face_auth_app

# Disk usage
docker system df
```

---

## 🔄 **Development Workflow**

### **Making Code Changes:**

1. **Edit your code**
   ```bash
   # Edit files in your IDE
   ```

2. **Rebuild and restart**
   ```bash
   # Stop current container
   docker-compose down
   
   # Rebuild with changes
   docker-compose up --build
   ```

3. **Test changes**
   ```bash
   # Check logs for errors
   docker logs face_auth_app
   
   # Test in browser
   # https://localhost:5000
   ```

### **Quick Restart (No Rebuild):**
```bash
# If you only changed Python code
docker-compose restart
```

### **Full Clean Restart:**
```bash
# Stop and remove everything
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

---

## 🗄️ **Database Management**

### **View Database**
```bash
# Access SQLite database
docker exec -it face_auth_app sqlite3 /app/instance/app.db

# List tables
.tables

# View users
SELECT * FROM user;

# Exit
.quit
```

### **Reset Database**
```bash
# Stop application
docker-compose down

# Delete database
rm instance/app.db

# Restart (will create new database)
docker-compose up
```

### **Backup Database**
```bash
# Backup
cp instance/app.db instance/app.db.backup

# Restore
cp instance/app.db.backup instance/app.db
```

---

## 🧪 **Testing**

### **Manual Testing:**

1. **Test User Registration**
   ```bash
   curl -k -X POST https://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"Test123!"}'
   ```

2. **Test User Login**
   ```bash
   curl -k -X POST https://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"Test123!"}'
   ```

3. **Test Health Check**
   ```bash
   curl -k https://localhost:5000/health
   ```

### **Automated Testing:**
```bash
# Run verification script
docker run --rm face_auth_system:latest python verify_setup.py
```

---

## 📦 **Production Deployment**

### **Environment Variables:**

Create a `.env` file:
```bash
# .env
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:////app/instance/app.db
FACE_RECOGNITION_TOLERANCE=0.6
FACE_ENCODING_MODEL=large
```

### **Production Start:**
```bash
# Load environment variables
docker-compose --env-file .env up -d

# Check logs
docker-compose logs -f
```

### **Production Checklist:**
- [ ] Change SECRET_KEY to random string
- [ ] Set FLASK_ENV=production
- [ ] Use real SSL certificate
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review security settings

---

## 🎯 **Quick Reference**

### **Essential Commands:**

| Action | Command |
|--------|---------|
| **Start** | `docker-compose up` |
| **Start (background)** | `docker-compose up -d` |
| **Stop** | `docker-compose down` |
| **Restart** | `docker-compose restart` |
| **Rebuild** | `docker-compose up --build` |
| **View logs** | `docker-compose logs -f` |
| **Check status** | `docker ps` |
| **Access shell** | `docker exec -it face_auth_app bash` |

### **URLs:**

| Page | URL |
|------|-----|
| **Home** | https://localhost:5000 |
| **Login** | https://localhost:5000/login |
| **Register** | https://localhost:5000/register |
| **Face Login** | https://localhost:5000/face-login |
| **Dashboard** | https://localhost:5000/dashboard |
| **Settings** | https://localhost:5000/settings |

---

## 🆘 **Getting Help**

### **Check Logs:**
```bash
# Application logs
docker logs face_auth_app

# Error logs only
docker logs face_auth_app 2>&1 | grep ERROR

# Authentication logs
docker logs face_auth_app | grep "face_auth.audit"
```

### **Debug Mode:**
```bash
# Run with debug output
docker-compose up

# Check environment
docker exec face_auth_app env

# Check Python version
docker exec face_auth_app python --version
```

### **Common Issues:**

1. **Can't access https://localhost:5000**
   - Check if container is running: `docker ps`
   - Check logs: `docker logs face_auth_app`
   - Try http://localhost:5000 (without SSL)

2. **Face recognition not working**
   - Check logs for "face_recognition library"
   - Verify image format (JPG/PNG)
   - Ensure face is clearly visible

3. **Database errors**
   - Check instance directory exists
   - Verify permissions: `ls -la instance/`
   - Try resetting database

---

## ✅ **Success Indicators**

You'll know the application is running correctly when you see:

```bash
✔ Container face_auth_app Running
face_auth_app  | Face Authentication System
face_auth_app  | URL: https://0.0.0.0:5000
face_auth_app  | Face recognizer initialized with face_recognition library
face_auth_app  | FaceService initialized (tolerance=0.35, model=large)
```

And you can access: **https://localhost:5000** in your browser!

---

## 🎉 **You're Ready!**

The application is now running and ready to use. Start by:

1. ✅ Opening https://localhost:5000
2. ✅ Registering a new user account
3. ✅ Uploading your face photo
4. ✅ Testing face login!

**Enjoy your secure face authentication system! 🔐**

---

**Last Updated**: 2026-04-22  
**Version**: 1.0  
**Status**: ✅ Production Ready
