---
inclusion: auto
---

# Development Rules

## 🏗️ Architecture Principles
- Follow modular and scalable architecture
- Separate concerns: Frontend, Backend, AI Service
- Backend follows MVC pattern: Routes → Controllers → Services → Models
- AI Service is completely decoupled from Flask
- Single entry point: `run.py`
- Configuration via `.env` file

## 📝 Code Quality
- Validate all inputs at controller level
- Handle errors gracefully with try/except
- Log all important operations (info, warning, error)
- Keep functions small and focused
- Write clean, readable code
- Add docstrings to all functions
- Use type hints where applicable

## 🔐 Security
- Store face embeddings only (never raw images)
- Hash passwords with bcrypt
- Use secure session management (Flask-Login)
- Validate and sanitize all user inputs
- Implement rate limiting for auth endpoints
- Use HTTPS in production

## 🔄 Execution Reliability
If execution fails:
1. Log the error with full context
2. Implement retry mechanism (max 3 attempts)
3. Return user-friendly error message
4. Rollback database changes
5. Do NOT crash the application

## 📊 Logging Requirements
- Use Python `logging` module (not print)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Log to file: `logs/faceauth.log`
- Rotate logs (max 10MB, keep 10 backups)

## 🎯 API Standards
- RESTful design
- Versioned URLs: `/api/v1/`
- Consistent response format (see dos_and_donts.md)
- Proper HTTP status codes
- Input validation on all endpoints
- Authentication required for protected routes

## 🧪 Edge Cases to Handle
- No face detected
- Multiple faces detected
- Low lighting conditions
- Camera access denied
- Face mismatch
- Invalid image input
- Network/API failure
- Slow AI processing
- Token/session expiration
