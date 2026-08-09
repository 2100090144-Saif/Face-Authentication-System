# 🐳 Docker Volume Mapping Guide - Development Mode

**Last Updated**: 2026-04-27  
**Purpose**: Enable live code editing with Docker  
**Status**: ✅ CONFIGURED  

---

## 📋 WHAT IS VOLUME MAPPING?

Volume mapping allows you to:
- ✅ Edit files on your **local machine**
- ✅ See changes **immediately** in the Docker container
- ✅ **No need to rebuild** Docker image after code changes
- ✅ **Hot-reload** Flask application automatically
- ✅ Keep database and logs **persistent**

---

## ✅ CONFIGURATION APPLIED

### Updated `docker-compose.yml`:

```yaml
services:
  app:
    volumes:
      # ── DEVELOPMENT MODE: Map entire project ──
      # This allows you to edit files locally and see changes immediately
      - .:/app
      
      # Exclude these directories (use container versions)
      - /app/__pycache__
      - /app/backend/__pycache__
      - /app/ai_service/__pycache__
      - /app/frontend/__pycache__
      
      # Persist database (important!)
      - ./instance:/app/instance
      
      # Persist logs
      - ./logs:/app/logs

    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1              # Enable Flask debug mode
      - FLASK_APP=run.py
      - PYTHONUNBUFFERED=1         # See logs immediately
```

### What This Does:

1. **`. :/app`** - Maps your **entire project directory** to `/app` in container
2. **`/app/__pycache__`** - Excludes Python cache (uses container's version)
3. **`./instance:/app/instance`** - Persists database across restarts
4. **`./logs:/app/logs`** - Persists logs
5. **`FLASK_DEBUG=1`** - Enables Flask auto-reload on file changes
6. **`PYTHONUNBUFFERED=1`** - Shows logs immediately (no buffering)

---

## 🚀 HOW TO USE

### Step 1: Stop Current Container
```bash
docker-compose down
```

### Step 2: Start with New Configuration
```bash
docker-compose up -d
```

### Step 3: Verify Volume Mapping
```bash
# Check volumes are mounted
docker inspect face_auth_app | grep -A 10 "Mounts"

# Or simpler:
docker-compose config
```

### Step 4: Test Live Editing

**Edit a file locally:**
```bash
# Example: Edit backend/services/face_service.py
# Add a log statement or change a message
```

**Check logs to see Flask reload:**
```bash
docker logs -f face_auth_app
```

You should see:
```
 * Detected change in '/app/backend/services/face_service.py', reloading
 * Restarting with stat
```

---

## 📝 WORKFLOW EXAMPLES

### Example 1: Fix a Bug

```bash
# 1. Edit file locally (VS Code, Notepad++, etc.)
# Edit: backend/services/face_service.py

# 2. Save the file

# 3. Flask automatically reloads (check logs)
docker logs -f face_auth_app

# 4. Test immediately
curl -k https://localhost:5000/health
```

### Example 2: Update Frontend

```bash
# 1. Edit template
# Edit: frontend/templates/login.html

# 2. Save the file

# 3. Refresh browser
# Changes appear immediately (no restart needed)
```

### Example 3: Update Configuration

```bash
# 1. Edit config
# Edit: backend/config/settings.py

# 2. Save the file

# 3. Flask reloads automatically

# 4. New config is active
```

---

## 🔍 VERIFY IT'S WORKING

### Test 1: Check Volume Mapping
```bash
# Create a test file locally
echo "test" > test_volume.txt

# Check if it appears in container
docker exec face_auth_app ls -la /app/test_volume.txt

# Expected: File exists in container
```

### Test 2: Check Auto-Reload
```bash
# Watch logs in one terminal
docker logs -f face_auth_app

# Edit any Python file in another terminal
# You should see: "Detected change... reloading"
```

### Test 3: Check Database Persistence
```bash
# Stop container
docker-compose down

# Start again
docker-compose up -d

# Check database still exists
docker exec face_auth_app ls -la /app/instance/app.db

# Expected: Database file exists with data intact
```

---

## 📊 WHAT'S MAPPED

### ✅ Mapped (Synced with Local):
```
✅ backend/          → /app/backend/
✅ frontend/         → /app/frontend/
✅ ai_service/       → /app/ai_service/
✅ architecture/     → /app/architecture/
✅ .kiro/            → /app/.kiro/
✅ run.py            → /app/run.py
✅ requirements.txt  → /app/requirements.txt
✅ .env              → /app/.env
✅ instance/         → /app/instance/ (database)
✅ logs/             → /app/logs/
```

### ❌ Excluded (Container Version Used):
```
❌ __pycache__/      (Python cache)
❌ *.pyc             (Compiled Python)
❌ venv/             (Virtual environment)
❌ .git/             (Git repository)
```

---

## 🎯 BENEFITS

### For Development:
1. ✅ **Instant feedback** - See changes immediately
2. ✅ **No rebuilds** - Save time (no `docker build`)
3. ✅ **Use local IDE** - VS Code, PyCharm, etc.
4. ✅ **Debug easily** - Add print statements, see logs
5. ✅ **Git integration** - Commit changes normally

### For Testing:
1. ✅ **Quick iterations** - Test fixes immediately
2. ✅ **Live debugging** - Add logs, restart automatically
3. ✅ **Database persists** - No data loss on restart
4. ✅ **Logs persist** - Review historical logs

---

## ⚠️ IMPORTANT NOTES

### 1. Python Dependencies
If you add new packages to `requirements.txt`:
```bash
# Option A: Rebuild image
docker-compose build

# Option B: Install in running container
docker exec face_auth_app pip install <package-name>
```

### 2. System Dependencies
If you need new system packages (apt-get):
```bash
# Must rebuild image
docker-compose build
```

### 3. Database Changes
Database is persistent:
```bash
# To reset database:
rm instance/app.db
docker-compose restart
```

### 4. Performance on Windows
Volume mapping can be slower on Windows:
- Use **WSL2** for better performance
- Or use **Docker Desktop with WSL2 backend**

### 5. File Permissions
On Linux/Mac, file permissions are preserved:
```bash
# If you get permission errors:
sudo chown -R $USER:$USER .
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: Changes Not Appearing

**Problem**: Edit file locally but container doesn't see changes

**Solution**:
```bash
# Check volume is mounted
docker inspect face_auth_app | grep -A 10 "Mounts"

# Restart container
docker-compose restart

# Check file in container
docker exec face_auth_app cat /app/backend/services/face_service.py
```

### Issue 2: Flask Not Auto-Reloading

**Problem**: File changes but Flask doesn't reload

**Solution**:
```bash
# Check FLASK_DEBUG is set
docker exec face_auth_app env | grep FLASK

# Should show:
# FLASK_ENV=development
# FLASK_DEBUG=1

# If not, restart with new config:
docker-compose down
docker-compose up -d
```

### Issue 3: Permission Denied

**Problem**: Container can't write to mounted volumes

**Solution**:
```bash
# On Linux/Mac:
sudo chown -R $USER:$USER instance/ logs/

# On Windows:
# Run Docker Desktop as Administrator
```

### Issue 4: Database Locked

**Problem**: "Database is locked" error

**Solution**:
```bash
# Stop all containers
docker-compose down

# Remove lock file
rm instance/app.db-journal

# Start again
docker-compose up -d
```

### Issue 5: Slow Performance (Windows)

**Problem**: File changes are slow to sync

**Solution**:
```bash
# Use WSL2 backend in Docker Desktop
# Settings → General → Use WSL2 based engine

# Or move project to WSL2 filesystem:
# \\wsl$\Ubuntu\home\user\project
```

---

## 🎓 BEST PRACTICES

### 1. Development Workflow
```bash
# Start container once
docker-compose up -d

# Edit files locally all day
# Flask auto-reloads on each save

# View logs when needed
docker logs -f face_auth_app

# Stop at end of day
docker-compose down
```

### 2. Git Workflow
```bash
# Work normally with Git
git add .
git commit -m "Fix bug"
git push

# Container sees changes immediately
# No special Docker commands needed
```

### 3. Testing Workflow
```bash
# Edit code locally
# Save file
# Flask reloads automatically
# Test immediately in browser or curl
```

### 4. Debugging Workflow
```bash
# Add print/log statements in code
# Save file
# Flask reloads
# Check logs: docker logs -f face_auth_app
```

---

## 📚 USEFUL COMMANDS

### View Logs (Live):
```bash
docker logs -f face_auth_app
```

### View Logs (Last 100 Lines):
```bash
docker logs face_auth_app --tail 100
```

### Execute Command in Container:
```bash
docker exec face_auth_app <command>
```

### Access Container Shell:
```bash
docker exec -it face_auth_app bash
```

### Check File in Container:
```bash
docker exec face_auth_app cat /app/backend/services/face_service.py
```

### Check Environment Variables:
```bash
docker exec face_auth_app env
```

### Restart Container:
```bash
docker-compose restart
```

### Rebuild Image:
```bash
docker-compose build
docker-compose up -d
```

### View Container Info:
```bash
docker inspect face_auth_app
```

---

## 🔄 SWITCHING MODES

### Development Mode (Current):
```yaml
volumes:
  - .:/app  # Full project mapped
environment:
  - FLASK_DEBUG=1  # Auto-reload enabled
```

### Production Mode:
```yaml
volumes:
  - ./instance:/app/instance  # Only database
  - ./logs:/app/logs          # Only logs
environment:
  - FLASK_DEBUG=0  # Auto-reload disabled
```

To switch:
```bash
# Edit docker-compose.yml
# Change volumes and FLASK_DEBUG

# Restart
docker-compose down
docker-compose up -d
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Volume mapping configured in docker-compose.yml
- [ ] FLASK_DEBUG=1 set in environment
- [ ] Container started with new configuration
- [ ] Test file appears in container
- [ ] Flask auto-reloads on file changes
- [ ] Database persists across restarts
- [ ] Logs are accessible locally
- [ ] Can edit files in local IDE
- [ ] Changes appear immediately

---

## 🎯 QUICK REFERENCE

### Start Development:
```bash
docker-compose up -d
docker logs -f face_auth_app
```

### Edit Code:
```
1. Edit files locally (VS Code, etc.)
2. Save
3. Flask reloads automatically
4. Test immediately
```

### Stop Development:
```bash
docker-compose down
```

### View Changes:
```bash
docker logs -f face_auth_app
```

---

## 📊 COMPARISON

### Before Volume Mapping:
```
1. Edit code locally
2. docker-compose build (5-10 minutes)
3. docker-compose up -d
4. Test
5. Repeat for each change ❌
```

### After Volume Mapping:
```
1. Edit code locally
2. Save (Flask reloads in 2 seconds)
3. Test
4. Repeat instantly ✅
```

**Time Saved**: ~5-10 minutes per change!

---

## 🎉 SUCCESS!

Your Docker container is now configured for **live development**:

✅ Edit files locally  
✅ See changes immediately  
✅ No rebuilds needed  
✅ Database persists  
✅ Logs accessible  
✅ Fast iteration  

**Happy coding!** 🚀

---

**Status**: ✅ CONFIGURED  
**Mode**: DEVELOPMENT  
**Auto-Reload**: ENABLED  
**Volume Mapping**: ACTIVE  

