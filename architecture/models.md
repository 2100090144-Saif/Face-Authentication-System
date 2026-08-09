# Database Models

## User Model
```python
class User:
    id: Integer (Primary Key)
    username: String(80) (Unique, Not Null)
    email: String(120) (Unique, Not Null)
    password_hash: String(255) (Not Null)
    face_recognition_enabled: Boolean (Default: False)
    created_at: DateTime (Default: now)
    updated_at: DateTime (Default: now, onupdate: now)
    
    # Relationships
    face_encodings: One-to-Many → FaceEncoding
```

## FaceEncoding Model
```python
class FaceEncoding:
    id: Integer (Primary Key)
    user_id: Integer (Foreign Key → User.id)
    encoding: PickleType (Stores numpy array)
    image_path: String(255) (Optional - for reference)
    created_at: DateTime (Default: now)
    is_active: Boolean (Default: True)
    
    # Relationships
    user: Many-to-One → User
```

## Session Model (handled by Flask-Login)
```python
# Flask-Login manages sessions automatically
# User sessions stored in secure cookies
```

## Indexes
- User.username (unique index)
- User.email (unique index)
- FaceEncoding.user_id (index for fast lookup)
- FaceEncoding.is_active (index for filtering)

## Constraints
- User.username: 3-80 characters, alphanumeric + underscore
- User.email: Valid email format
- User.password: Minimum 8 characters (enforced at application level)
- FaceEncoding.user_id: Must reference existing user (foreign key)

## Data Flow

### Registration
1. User submits username, email, password
2. Password hashed with bcrypt
3. User record created
4. User logged in automatically

### Face Registration
1. User must be logged in
2. Capture face image
3. Generate face encoding
4. Store encoding in FaceEncoding table
5. Set user.face_recognition_enabled = True

### Face Login
1. Capture face image
2. Generate face encoding
3. Query all active face encodings
4. Compare with stored encodings
5. If match found (confidence > threshold):
   - Get associated user
   - Log user in
6. Else: Show error

### Password Login
1. User submits username/password
2. Query user by username
3. Verify password hash
4. If valid: Log user in
5. Else: Show error
