---
inclusion: auto
---

# Dos and Don'ts

## ✅ DO:
- Analyze existing code before changes
- Improve structure incrementally
- Secure biometric data properly
- Optimize performance for face recognition
- Keep UI simple and intuitive
- Add proper logging and monitoring
- Validate all API inputs and outputs
- Write reusable and testable code
- Store only face embeddings (never raw images)
- Use consistent API response format
- Handle errors gracefully with retry mechanisms
- Follow MVC pattern strictly

## ❌ DON'T:
- Don't rewrite entire project unnecessarily
- Don't mix business logic with UI
- Don't tightly couple services
- Don't store raw face images unnecessarily
- Don't ignore error handling
- Don't expose sensitive data in logs or APIs
- Don't hardcode configuration values
- Don't skip input validation
- Don't let the app crash on invalid input
- Don't block UI during long operations

## 🔒 Security Rules:
- Store only face embeddings (128-d vectors)
- Hash passwords with bcrypt
- Use HTTPS for camera access
- Implement rate limiting on auth endpoints
- Validate all file uploads
- Sanitize all user inputs
- Use secure session management

## 📐 API Response Format (MANDATORY):
```json
{
  "success": true,
  "data": {},
  "message": "Human readable message",
  "error": null
}
```

## 🔄 Error Handling Rules:
- Catch all exceptions
- Log errors with context
- Return user-friendly messages
- Implement retry mechanism for AI processing
- Never expose stack traces to users
- Always rollback database transactions on error
