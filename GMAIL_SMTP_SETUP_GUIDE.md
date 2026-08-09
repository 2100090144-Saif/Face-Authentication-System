# 📧 Gmail SMTP Setup Guide - FREE & EASY

## ⚠️ IMPORTANT: Gmail Security Update

Gmail no longer allows regular passwords for SMTP access. You need to create an **App Password** (it's free and takes 2 minutes).

---

## 🚀 QUICK SETUP (2 Minutes)

### Step 1: Enable 2-Factor Authentication

1. Go to: https://myaccount.google.com/security
2. Scroll to "How you sign in to Google"
3. Click "2-Step Verification"
4. Follow the setup (use your phone number)
5. ✅ Done!

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
   - Or search "App passwords" in Google Account settings
2. You might need to sign in again
3. In "Select app" dropdown: Choose **"Mail"**
4. In "Select device" dropdown: Choose **"Other (Custom name)"**
5. Type: **"Face Auth System"**
6. Click **"Generate"**
7. 📋 **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 3: Update .env File

Open your `.env` file and update the password:

```env
MAIL_PASSWORD=abcdefghijklmnop
```

**Note**: Remove the spaces from the app password!

### Step 4: Restart Container

```bash
docker-compose restart
```

---

## 🎯 YOUR CURRENT CONFIGURATION

Your `.env` file is already configured with:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=mdsaif83118@gmail.com
MAIL_PASSWORD=Saif@1234  ← NEEDS TO BE APP PASSWORD
MAIL_DEFAULT_SENDER=mdsaif83118@gmail.com
```

**What to change**: Replace `Saif@1234` with the 16-character app password from Step 2.

---

## 🧪 TEST IT

After updating the app password and restarting:

1. Go to: https://localhost:5000/login
2. Click "Forgot Password?"
3. Enter: `mdsaif83118@gmail.com`
4. Click "Send Reset Link"
5. Check your Gmail inbox! 📬

---

## ❓ WHY APP PASSWORD?

Google requires app passwords for security reasons:
- ✅ More secure than regular password
- ✅ Can be revoked anytime
- ✅ Doesn't give full account access
- ✅ **100% FREE** - no payment required

---

## 🐛 TROUBLESHOOTING

### "Invalid credentials" error?
- Make sure you created the app password
- Remove spaces from the app password
- Use the app password, not your regular Gmail password

### Can't find "App passwords" option?
- Make sure 2-Factor Authentication is enabled first
- Wait a few minutes after enabling 2FA
- Try this direct link: https://myaccount.google.com/apppasswords

### Still not working?
1. Check Docker logs: `docker logs face_auth_app --tail 50`
2. Verify .env file has correct email
3. Make sure container restarted: `docker-compose restart`

---

## 📱 ALTERNATIVE: Use Gmail Web Interface

If you don't want to set up app passwords, you can:
1. Check the reset token in Docker logs
2. Manually construct the reset URL
3. Use it to reset the password

But setting up the app password is much easier! 😊

---

## ✅ CHECKLIST

- [ ] Enable 2-Factor Authentication on Gmail
- [ ] Generate App Password
- [ ] Copy the 16-character password
- [ ] Update `.env` file with app password
- [ ] Restart Docker container
- [ ] Test forgot password feature
- [ ] Check Gmail inbox

---

## 🎉 ONCE CONFIGURED

After setup, the forgot password feature will:
- ✅ Send professional HTML emails
- ✅ Include secure reset links
- ✅ Work automatically
- ✅ Be 100% free forever

---

**Your Email**: mdsaif83118@gmail.com  
**SMTP Server**: smtp.gmail.com (FREE)  
**Cost**: $0.00 (Completely Free)  
**Setup Time**: 2 minutes

---

## 🔗 USEFUL LINKS

- Gmail Security: https://myaccount.google.com/security
- App Passwords: https://myaccount.google.com/apppasswords
- Gmail Help: https://support.google.com/accounts/answer/185833

---

**Status**: ⏳ Waiting for App Password  
**Next Step**: Generate app password and update .env file
