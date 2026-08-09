# Architecture Plan

## Overview
Restructure the existing monolithic face authentication app into a scalable, production-ready system with proper separation of concerns.

## Current State Analysis
- **Existing**: Monolithic Flask app with basic face detection (no recognition)
- **Issues**: No user management, no database, no actual face matching, security vulnerabilities
- **Assets to Reuse**: Haarcascade model, basic Flask structure, HTML templates (refactored)

## Target Architecture

### Three-Tier Architecture
```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│  (HTML/CSS/JS - Modern, Responsive UI)                 │
│  - Login Page (Password + Face Option)                 │
│  - Registration Page                                    │
│  - Dashboard/Welcome Page                               │
│  - Settings Page (Enable/Disable Face Login)           │
│  - Face Registration Page                               │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (Flask)                       │
│  - Routes (Blueprints)                                  │
│  - Controllers (Request handling)                       │
│  - Services (Business logic)                            │
│  - Models (Database ORM)                                │
│  - Middleware (Auth, validation)                        │
│  - Config (Environment-based)                           │
└─────────────────────────────────────────────────────────┘
                          ↓ Internal API
┌─────────────────────────────────────────────────────────┐
│                   AI SERVICE (Python)                   │
│  - Face Detection Module                                │
│  - Face Recognition Module                              │
│  - Face Encoding Storage                                │
│  - Model Management                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   DATABASE (SQLite)                     │
│  - Users Table                                          │
│  - Face Encodings Table                                 │
│  - Settings Table                                       │
└─────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Foundation
- Set up project structure
- Create database models
- Implement user authentication (password-based)
- Create basic frontend templates

### Phase 2: Face Recognition Service
- Implement face detection module
- Implement face encoding generation
- Implement face matching/recognition
- Create face registration flow

### Phase 3: Integration
- Integrate face recognition with authentication
- Create settings page for face login toggle
- Implement face-based login flow
- Add proper error handling

### Phase 4: Polish
- Add logging
- Improve UI/UX
- Add validation
- Security hardening
- Performance optimization

## Key Features

### User Authentication
- Traditional username/password login
- Secure password hashing (bcrypt)
- Session management
- Registration flow

### Face Recognition
- Optional feature (can be enabled/disabled per user)
- Face registration (capture and store encodings)
- Face-based login
- Confidence threshold for matching
- Fallback to password if face recognition fails

### Settings Management
- User profile page
- Enable/disable face recognition
- Re-register face
- Delete face data

## Technology Stack
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt
- **AI**: OpenCV, face_recognition (dlib)
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla or lightweight framework)
- **Security**: bcrypt, secure sessions, CSRF protection
