# Application Flow

## User Registration Flow
```
1. User visits /register
2. User fills form (username, email, password)
3. Frontend validates input
4. POST /api/v1/auth/register
5. Backend validates input
6. Backend hashes password
7. Backend creates user in database
8. Backend creates session
9. Redirect to /dashboard
```

## Password Login Flow
```
1. User visits /login
2. User enters username and password
3. Frontend validates input
4. POST /api/v1/auth/login
5. Backend queries user by username
6. Backend verifies password hash
7. If valid:
   - Create session
   - Return user data
   - Redirect to /dashboard
8. If invalid:
   - Return error
   - Show error message
```

## Face Registration Flow
```
1. User logged in and visits /settings
2. User clicks "Enable Face Recognition"
3. Redirect to /face/register
4. Frontend requests camera access
5. User positions face in frame
6. Face detection highlights face
7. User clicks "Capture"
8. Frontend captures image
9. POST /api/v1/face/register (with image)
10. Backend receives image
11. AI Service detects face
12. AI Service generates encoding
13. Backend stores encoding in database
14. Backend sets user.face_recognition_enabled = True
15. Return success
16. Redirect to /settings
```

## Face Login Flow
```
1. User visits /login
2. User clicks "Login with Face"
3. Redirect to /face/login
4. Frontend requests camera access
5. User positions face in frame
6. Face detection highlights face
7. User clicks "Authenticate"
8. Frontend captures image
9. POST /api/v1/face/login (with image)
10. Backend receives image
11. AI Service detects face
12. AI Service generates encoding
13. AI Service compares with all stored encodings
14. If match found (confidence > threshold):
    - Get associated user
    - Create session
    - Return user data
    - Redirect to /dashboard
15. If no match:
    - Return error
    - Show "Face not recognized" message
    - Offer password login option
```

## Settings Management Flow
```
1. User logged in and visits /settings
2. Frontend displays current settings:
   - Face recognition status (enabled/disabled)
   - Number of face encodings
3. User can:
   a. Enable face recognition → Redirect to /face/register
   b. Disable face recognition → PUT /api/v1/settings/face-recognition
   c. Re-register face → DELETE encodings → Redirect to /face/register
   d. Delete face data → DELETE /api/v1/face/encodings
```

## Dashboard Flow
```
1. User logged in and visits /dashboard
2. Frontend displays:
   - Welcome message with username
   - Quick stats
   - Navigation to settings
   - Logout button
3. User can:
   - Go to settings
   - Logout
```

## Logout Flow
```
1. User clicks logout
2. POST /api/v1/auth/logout
3. Backend destroys session
4. Redirect to /login
```

## Error Handling Flows

### Camera Access Denied
```
1. User denies camera permission
2. Frontend shows error message
3. Frontend offers alternative:
   - Use password login
   - Instructions to enable camera
```

### No Face Detected
```
1. AI Service cannot detect face in image
2. Backend returns error
3. Frontend shows message:
   - "No face detected"
   - "Please ensure good lighting"
   - "Position face in frame"
4. User can retry
```

### Face Not Recognized
```
1. AI Service cannot match face
2. Backend returns error
3. Frontend shows message:
   - "Face not recognized"
   - "Try again or use password"
4. User can:
   - Retry face login
   - Switch to password login
```

### Network Error
```
1. API request fails
2. Frontend catches error
3. Frontend shows message:
   - "Connection error"
   - "Please check your internet"
4. User can retry
```

## Security Flows

### Session Validation
```
Every protected route:
1. Check if session exists
2. Check if session is valid
3. Check if user still exists
4. If any check fails:
   - Destroy session
   - Redirect to /login
```

### Rate Limiting
```
For authentication endpoints:
1. Track requests per IP
2. If > 5 failed attempts in 15 minutes:
   - Return 429 Too Many Requests
   - Block for 15 minutes
3. Reset counter on successful login
```

### Input Validation
```
For all user inputs:
1. Validate on frontend (immediate feedback)
2. Validate on backend (security)
3. Sanitize inputs
4. Return specific error messages
```
