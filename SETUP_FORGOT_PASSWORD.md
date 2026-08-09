# 🚀 Quick Setup Guide - Forgot Password Feature

**Time Required**: 5-10 minutes  
**Difficulty**: Easy  

---

## ✅ STEP-BY-STEP SETUP

### **Step 1: Install Flask-Mail** (1 minute)

```bash
pip install Flask-Mail==0.9.1
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

---

### **Step 2: Configure Email** (3 minutes)

#### **Option A: Gmail (Recommended for Testing)**

1. **Enable 2-Factor Authentication**:
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Update `.env` file**:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

#### **Option B: Other Providers**

**Outlook**:
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

**Yahoo**:
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

---

### **Step 3: Update Database** (1 minute)

The database will auto-update when you start the app:

```bash
python run.py
```

Or manually:
```python
from backend.app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

---

### **Step 4: Test the Feature** (2 minutes)

1. **Start the application**:
```bash
python run.py
```

2. **Go to login page**:
```
http://localhost:5000/login
```

3. **Click "Forgot Password?"**

4. **Enter your email and submit**

5. **Check your email** (should arrive within 1 minute)

6. **Click the reset link**

7. **Enter new password**

8. **Login with new password** ✅

---

## 🎯 QUICK TEST

```bash
# Test API endpoint
curl -X POST http://localhost:5000/api/v1/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@gmail.com"}'

# Expected response:
# {
#   "success": true,
#   "message": "If an account exists with this email, you will receive a password reset link"
# }
```

---

## 🐛 TROUBLESHOOTING

### **Email not sending?**

1. **Check `.env` file**:
```bash
cat .env | grep MAIL
```

2. **Verify credentials**:
   - Gmail: Use App Password (not regular password)
   - Enable 2FA first

3. **Check logs**:
```bash
# Look for email errors
tail -f logs/faceauth.log
```

4. **Test SMTP connection**:
```python
from flask_mail import Mail, Message
from backend.app import create_app

app = create_app()
mail = Mail(app)

with app.app_context():
    msg = Message('Test', recipients=['your-email@gmail.com'])
    msg.body = 'Test email'
    mail.send(msg)
    print("Email sent!")
```

---

## ✅ SUCCESS CHECKLIST

- [ ] Flask-Mail installed
- [ ] Email configured in `.env`
- [ ] Application starts without errors
- [ ] "Forgot Password?" link visible on login page
- [ ] Can submit email on forgot password page
- [ ] Email received within 1 minute
- [ ] Reset link works
- [ ] Can change password
- [ ] Confirmation email received
- [ ] Can login with new password

---

## 📧 EMAIL CONFIGURATION EXAMPLES

### **Gmail**:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=myapp@gmail.com
MAIL_PASSWORD=abcd-efgh-ijkl-mnop
MAIL_DEFAULT_SENDER=myapp@gmail.com
```

### **Outlook**:
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=myapp@outlook.com
MAIL_PASSWORD=mypassword
MAIL_DEFAULT_SENDER=myapp@outlook.com
```

### **SendGrid (Production)**:
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.xxxxxxxxxxxxx
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

---

## 🎉 DONE!

Your forgot password feature is now ready to use!

**Next Steps**:
1. Test with real users
2. Monitor email delivery
3. Consider production email service (SendGrid, Mailgun)

---

**Need help?** Check `FORGOT_PASSWORD_FEATURE.md` for detailed documentation.

