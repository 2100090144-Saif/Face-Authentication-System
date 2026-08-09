# 📸 Postman Guide: Face Login

## 🎯 Issue

Face registration works in Postman, but face login says "image is required".

---

## ✅ SOLUTION: Correct Postman Setup

### Face Login Request Configuration:

**1. Method**: `POST`

**2. URL**: `https://localhost:5000/api/v1/face/login`

**3. Body Tab**:
- Select **"form-data"** (NOT "binary", NOT "raw")
- Click "KEY" field
- Type: `image` (exactly this, lowercase)
- **IMPORTANT**: Change the dropdown on the right from "Text" to **"File"**
- Click "Select Files" button that appears
- Choose your face image file

**4. Headers** (Auto-added by Postman):
- `Content-Type: multipart/form-data`

**5. SSL Certificate** (if needed):
- Settings → SSL certificate verification → OFF

---

## 🔍 Common Mistakes

### ❌ WRONG:

1. **Wrong field name**:
   ```
   Field: "Image"     ← Capital I (wrong!)
   Field: "file"      ← Wrong name
   Field: "photo"     ← Wrong name
   ```

2. **Wrong body type**:
   ```
   Body: "binary"     ← Wrong!
   Body: "raw"        ← Wrong!
   ```

3. **Text instead of File**:
   ```
   Type: "Text"       ← Wrong! Must be "File"
   ```

### ✅ CORRECT:

```
Body: form-data
Field Name: image (lowercase)
Type: File (not Text)
```

---

## 📋 Step-by-Step Postman Setup

### Step 1: Create New Request
1. Click "+" to create new request
2. Select **POST** method

### Step 2: Enter URL
```
https://localhost:5000/api/v1/face/login
```

### Step 3: Configure Body
1. Click **"Body"** tab
2. Select **"form-data"** radio button
3. In the KEY field, type: `image`
4. **CRITICAL**: Click the dropdown on the right (says "Text")
5. Change it to **"File"**
6. You'll see "Select Files" button appear
7. Click "Select Files" and choose your image

### Step 4: Disable SSL Verification (if using self-signed cert)
1. Go to Postman Settings (⚙️ icon)
2. Turn off "SSL certificate verification"
3. Close settings

### Step 5: Send Request
1. Click **"Send"** button
2. Check response

---

## 📸 Visual Guide

### Correct Postman Body Configuration:

```
┌─────────────────────────────────────────┐
│ Params  Authorization  Headers  Body    │
├─────────────────────────────────────────┤
│ ○ none                                  │
│ ○ form-data         ← SELECT THIS      │
│ ○ x-www-form-urlencoded                │
│ ○ raw                                   │
│ ○ binary                                │
│ ○ GraphQL                               │
├─────────────────────────────────────────┤
│ KEY          TYPE     VALUE             │
│ image        File     [Select Files]    │
│              ↑                           │
│              └── CHANGE FROM "Text"     │
└─────────────────────────────────────────┘
```

---

## 🧪 Test Both Endpoints

### 1. Face Registration (Requires Login First)

**URL**: `POST https://localhost:5000/api/v1/face/register`

**Headers**:
```
Authorization: Bearer <your-session-cookie>
```

**Body**: form-data
```
Key: image
Type: File
Value: [Select your face image]
```

**Response** (Success):
```json
{
  "status": "success",
  "data": {
    "encoding_id": 8,
    "message": "Face registered successfully"
  }
}
```

### 2. Face Login (No Login Required)

**URL**: `POST https://localhost:5000/api/v1/face/login`

**Body**: form-data
```
Key: image
Type: File
Value: [Select your face image]
```

**Response** (Success):
```json
{
  "status": "success",
  "data": {
    "user_id": 7,
    "username": "saif4u_12",
    "confidence": 85.5
  }
}
```

---

## 🐛 Debug Steps

### 1. Check What Postman is Sending

Look at Docker logs after sending request:
```bash
docker logs face_auth_app --tail 20
```

You should see something like:
```
ImmutableMultiDict([('image', <FileStorage: 'photo.jpg' ('image/jpeg')>)])
```

### 2. If You See "ImmutableMultiDict([])"

This means NO file was sent. Check:
- Field name is exactly `image`
- Type is set to "File" (not "Text")
- You selected a file

### 3. If You See Different Field Name

Example: `ImmutableMultiDict([('photo', ...)])`

Change your field name from `photo` to `image`

---

## 📝 Complete Working Example

### Request:
```
POST https://localhost:5000/api/v1/face/login
Content-Type: multipart/form-data

Body (form-data):
┌──────────┬────────┬──────────────────┐
│ KEY      │ TYPE   │ VALUE            │
├──────────┼────────┼──────────────────┤
│ image    │ File   │ my_face.jpg      │
└──────────┴────────┴──────────────────┘
```

### Response (Success):
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "user_id": 7,
    "username": "saif4u_12",
    "email": "saif@example.com",
    "confidence": 87.3,
    "face_recognition_enabled": true
  }
}
```

### Response (Error - No Image):
```json
{
  "status": "error",
  "message": "Image file is required"
}
```

---

## ⚠️ Important Notes

1. **Field name is case-sensitive**: Must be `image` (lowercase)

2. **File type must be image**: jpg, jpeg, png (not pdf, doc, etc.)

3. **Image size**: Keep under 10 MB

4. **Face must be visible**: Clear, well-lit photo

5. **Session cookies**: Face login doesn't need login, but face registration does

---

## 🔄 Comparison: Registration vs Login

| Feature | Face Registration | Face Login |
|---------|------------------|------------|
| **Endpoint** | `/api/v1/face/register` | `/api/v1/face/login` |
| **Requires Login** | ✅ Yes | ❌ No |
| **Field Name** | `image` | `image` |
| **Body Type** | form-data | form-data |
| **Purpose** | Store face | Verify face |

---

## ✅ Quick Checklist

Before sending request, verify:

- [ ] Method is POST
- [ ] URL is correct (`/api/v1/face/login`)
- [ ] Body type is "form-data"
- [ ] Field name is exactly `image` (lowercase)
- [ ] Type is changed to "File" (not "Text")
- [ ] Image file is selected
- [ ] SSL verification is off (if self-signed cert)

---

## 🎯 Still Not Working?

Try this curl command to test if API works:

```bash
curl -k -X POST https://localhost:5000/api/v1/face/login \
  -F "image=@/path/to/your/photo.jpg"
```

If curl works but Postman doesn't, it's a Postman configuration issue.

---

**Status**: This guide should fix your "image is required" error in Postman!
