---
inclusion: auto
---

# Best Practices

## 🎨 Backend (Flask)
- Use MVC pattern with service layer
- Keep controllers thin (delegate to services)
- Keep services focused (single responsibility)
- Use Flask Blueprints for route organization
- Implement proper error handling middleware
- Use async/await for long-running operations (if needed)
- Always use ORM (SQLAlchemy) - never raw SQL

## 🖼️ Frontend
- Use component-based templates (base.html + extends)
- Separate concerns (HTML structure, CSS styling, JS behavior)
- Handle all edge cases (camera failure, network errors)
- Provide clear user feedback (loading states, error messages)
- Implement progressive enhancement
- Use HTTPS for camera access

## 🤖 AI Service
- Keep AI logic separate from web logic
- Use proper model management (lazy loading)
- Handle model loading errors gracefully
- Implement fallback mechanisms
- Log all AI operations for debugging
- Optimize for performance (skip frames, resize images)
- Return confidence scores with results

## 📡 API Design
- Keep API response consistent (see steering/dos_and_donts.md)
- Use proper HTTP status codes:
  - 200 OK - Success
  - 201 Created - Resource created
  - 400 Bad Request - Validation error
  - 401 Unauthorized - Auth required
  - 500 Internal Server Error - Server error
- Version your APIs (`/api/v1/`)
- Document all endpoints
- Implement pagination for list endpoints

## 🗄️ Database
- Use migrations for schema changes
- Index frequently queried fields
- Use relationships properly
- Avoid N+1 queries
- Keep models focused
- Always use transactions for multi-step operations

## 🔍 Error Handling
```python
try:
    # Operation
    result = service.do_something()
    db.session.commit()
    return success_response(result)
except ValidationError as e:
    logger.warning(f"Validation error: {str(e)}")
    return error_response(str(e), status_code=400)
except Exception as e:
    db.session.rollback()
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return error_response("An error occurred", status_code=500)
```

## 📝 Logging Best Practices
```python
import logging

logger = logging.getLogger(__name__)

# Good logging
logger.info(f"User {username} logged in successfully")
logger.warning(f"Failed login attempt for user: {username}")
logger.error(f"Database error: {str(e)}", exc_info=True)

# Bad logging
print("User logged in")  # Don't use print
logger.info(f"Password: {password}")  # Don't log sensitive data
```

## 🔄 Retry Mechanism
```python
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def process_face_with_retry(image_data):
    """Retry face processing up to 3 times"""
    return face_service.process(image_data)
```

## 🧪 Testing
- Write unit tests for services
- Write integration tests for APIs
- Test edge cases
- Mock external dependencies
- Aim for high coverage on critical paths
