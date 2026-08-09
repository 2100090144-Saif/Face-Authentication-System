# API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Response Format
All API responses follow this structure:
```json
{
  "success": true/false,
  "data": {...},
  "message": "Human-readable message",
  "error": null or "error details"
}
```

## HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

---

## Authentication Endpoints

### POST /api/v1/auth/register
Register a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "face_recognition_enabled": false
    }
  },
  "message": "Registration successful",
  "error": null
}
```

### POST /api/v1/auth/login
Login with username and password.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "face_recognition_enabled": true
    }
  },
  "message": "Login successful",
  "error": null
}
```

### POST /api/v1/auth/logout
Logout current user.

**Response (200):**`
```json
{
  "success": true,
  "data": null,
  "message": "Logout successful",
  "error": null
}
```

### GET /api/v1/auth/me
Get current user information (requires authentication).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "face_recognition_enabled": true
    }
  },
  "message": "User retrieved",
  "error": null
}
```

---

## Face Recognition Endpoints

### POST /api/v1/face/register
Register user's face (requires authentication).

**Request Body (multipart/form-data):**
```
image: <file> (captured face image)
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "encoding_id": 1,
    "message": "Face registered successfully"
  },
  "message": "Face registration successful",
  "error": null
}
```

### POST /api/v1/face/login
Login using face recognition.

**Request Body (multipart/form-data):**
```
image: <file> (captured face image)
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "confidence": 0.95
  },
  "message": "Face authentication successful",
  "error": null
}
```

### DELETE /api/v1/face/encodings
Delete all face encodings for current user (requires authentication).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "deleted_count": 3
  },
  "message": "Face encodings deleted",
  "error": null
}
```

### GET /api/v1/face/encodings
Get list of face encodings for current user (requires authentication).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "encodings": [
      {
        "id": 1,
        "created_at": "2026-04-20T10:30:00",
        "is_active": true
      }
    ]
  },
  "message": "Encodings retrieved",
  "error": null
}
```

---

## Settings Endpoints

### PUT /api/v1/settings/face-recognition
Enable or disable face recognition for current user (requires authentication).

**Request Body:**
```json
{
  "enabled": true
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "face_recognition_enabled": true
  },
  "message": "Face recognition settings updated",
  "error": null
}
```

### GET /api/v1/settings
Get user settings (requires authentication).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "face_recognition_enabled": true,
    "has_face_encodings": true,
    "encoding_count": 3
  },
  "message": "Settings retrieved",
  "error": null
}
```

---

## Error Response Examples

### 400 Bad Request
```json
{
  "success": false,
  "data": null,
  "message": "Validation error",
  "error": "Password must be at least 8 characters"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "data": null,
  "message": "Authentication required",
  "error": "Please login to access this resource"
}
```

### 404 Not Found
```json
{
  "success": false,
  "data": null,
  "message": "User not found",
  "error": "No user found with username: john_doe"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "data": null,
  "message": "Internal server error",
  "error": "An unexpected error occurred"
}
```
