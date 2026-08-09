# 🚀 QUICK START: Forgot Password Feature

## ✅ STATUS: READY TO USE

The forgot password feature is **fully implemented** and **working**. All code is in place, database is migrated, and the application is running.

---

## 🎯 IMMEDIATE USAGE (Without Email)

You can use the feature **right now** without configuring email:

### 1. Open Login Page
```
https://localhost:5000/login
```

### 2. Click "Forgot Password?" Link

### 3. Enter Email Address
- The system will generate a reset token
- Token will be saved to database
- Email sending will fail (but that's OK for testing)

### 4. Get Token from Logs
```bash
docker logs face_auth_app --tail 50
```
Look for: `Reset token generated: <token-here>`

### 5. Use Token Manually
```
https://localhost:5000/auth/reset-password/<token-here>
```

---

## 📧 ENABLE EMAIL SENDING (5 Minutes)

To actually send password reset emails:

### Step 1: Get Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to "App passwords"
4. Generate password for "Mail"
5. Copy the 16-character password

### Step 2: Update .env File
```bash
# Open .env file and add:
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Step 3: Restart Container
```bash
docker-compose restart
```

### Step 4: Test It
1. Go to login page
2. Click "Forgot Password?"
3. Enter your email
4. Check your inbox
5. Click the reset link
6. Enter new password

---

## 🔗 IMPORTANT URLS

| Page | URL |
|------|-----|
| Login | https://localhost:5000/login |
| Forgot Password | https://localhost:5000/auth/forgot-password |
| Reset Password | https://localhost:5000/auth/reset-password/TOKEN |
| Dashboard | https://localhost:5000/dashboard |

---

## 🧪 API ENDPOINTS

### Request Password Reset
```bash
POST /api/v1/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response**:
```json
{
  "message": "If your email exists, you will receive a password reset link"
}
```

### Reset Password
```bash
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "token": "reset-token-here",
  "new_password": "NewPassword123!"
}
```

**Response**:
```json
{
  "message": "Password has been reset successfully"
}
```

---

## 🔒 SECURITY FEATURES

✅ Secure random tokens (32 bytes)  
✅ Tokens expire after 1 hour  
✅ Single-use tokens  
✅ No user enumeration  
✅ Password validation  
✅ Rate limiting  

---

## 📊 WHAT'S INCLUDED

### Backend:
- ✅ Email service with HTML templates
- ✅ Password reset controller
- ✅ Token generation and validation
- ✅ Database models updated
- ✅ API routes configured

### Frontend:
- ✅ Forgot password form
- ✅ Reset password form
- ✅ Login page updated
- ✅ Success/error messages
- ✅ Responsive design

### Database:
- ✅ reset_token column (indexed)
- ✅ reset_token_expiry column
- ✅ Migration completed

---

## 🐛 TROUBLESHOOTING

### Email Not Sending?
**Check**: `.env` file has correct SMTP settings  
**Check**: Using Gmail App Password (not regular password)  
**Check**: Docker logs for errors: `docker logs face_auth_app`

### Token Invalid?
**Check**: Token expires after 1 hour  
**Solution**: Request new reset link

### Page Not Loading?
**Check**: Container is running: `docker ps`  
**Solution**: Restart container: `docker-compose restart`

### Database Error?
**Check**: Migration was successful  
**Solution**: Re-run migration: `docker exec face_auth_app python migrate_password_reset.py`

---

## 📞 SUPPORT

### View Logs
```bash
# All logs
docker logs face_auth_app

# Last 50 lines
docker logs face_auth_app --tail 50

# Follow logs (live)
docker logs face_auth_app -f
```

### Check Database
```bash
docker exec face_auth_app python -c "from backend.app import create_app, db; app = create_app(); app.app_context().push(); inspector = db.inspect(db.engine); print([col['name'] for col in inspector.get_columns('users')])"
```

### Check Routes
```bash
docker exec face_auth_app python -c "from backend.app import create_app; app = create_app(); [print(rule) for rule in app.url_map.iter_rules() if 'password' in str(rule)]"
```

---

## 🎉 SUMMARY

| Component | Status |
|-----------|--------|
| Database Migration | ✅ Complete |
| Backend Code | ✅ Complete |
| Frontend Templates | ✅ Complete |
| API Routes | ✅ Complete |
| Application Running | ✅ Yes |
| Feature Working | ✅ Yes |
| Email Configured | ⏳ Optional |

---

## 📚 MORE DOCUMENTATION

- `FORGOT_PASSWORD_COMPLETE.md` - Full implementation details
- `PROBLEM_FIXED_SUMMARY.md` - Migration fix details
- `SETUP_FORGOT_PASSWORD.md` - Detailed setup guide
- `FORGOT_PASSWORD_FEATURE.md` - Feature documentation

---

**Last Updated**: May 8, 2026  
**Status**: ✅ READY TO USE  
**Next Step**: Configure email settings (optional)
