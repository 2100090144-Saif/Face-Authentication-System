# Architecture Decisions

## Technology Choices

### Backend Framework: Flask
**Decision**: Use Flask instead of Django or FastAPI

**Rationale**:
- Lightweight and flexible
- Easy to structure with Blueprints
- Excellent ecosystem (Flask-Login, Flask-SQLAlchemy)
- Existing codebase already uses Flask
- Perfect for small to medium applications

**Trade-offs**:
- Less built-in features than Django
- Need to add extensions manually
- More setup required

### Database: SQLite (with PostgreSQL path)
**Decision**: Start with SQLite, design for easy PostgreSQL migration

**Rationale**:
- Zero configuration for development
- File-based, easy to backup
- Sufficient for small to medium user base
- SQLAlchemy makes migration to PostgreSQL trivial
- No additional infrastructure needed

**Trade-offs**:
- Limited concurrent writes
- Not suitable for high-traffic production
- Need to migrate for scale

### Face Recognition Library: face_recognition (dlib)
**Decision**: Use face_recognition library instead of pure OpenCV

**Rationale**:
- Higher accuracy than Haar Cascades
- Built on dlib's state-of-the-art face recognition
- Simple API for encoding and comparison
- Well-maintained and documented
- Industry-standard approach

**Trade-offs**:
- Larger dependency (dlib)
- Slower than Haar Cascades
- More CPU/memory intensive
- Requires compilation on some systems

### Session Management: Flask-Login
**Decision**: Use Flask-Login for session management

**Rationale**:
- Industry standard for Flask
- Handles session lifecycle automatically
- Integrates with Flask-SQLAlchemy
- Provides decorators for route protection
- Secure by default

**Trade-offs**:
- Tied to Flask ecosystem
- Cookie-based (not JWT)

### Password Hashing: bcrypt
**Decision**: Use bcrypt for password hashing

**Rationale**:
- Industry standard
- Adaptive (can increase rounds as hardware improves)
- Built-in salt generation
- Resistant to rainbow table attacks
- Flask-Bcrypt provides easy integration

**Trade-offs**:
- Slower than SHA-256 (by design)
- Fixed output length

## Architecture Patterns

### Pattern: Three-Tier Architecture
**Decision**: Separate Frontend, Backend, and AI Service

**Rationale**:
- Clear separation of concerns
- Each tier can be scaled independently
- Easier to test and maintain
- AI service can be reused by other applications
- Frontend can be replaced without touching backend

### Pattern: MVC in Backend
**Decision**: Use Model-View-Controller pattern

**Rationale**:
- Industry standard for web applications
- Clear separation of data, logic, and presentation
- Easier to test business logic
- Better code organization
- Easier onboarding for new developers

### Pattern: Service Layer
**Decision**: Add service layer between controllers and models

**Rationale**:
- Encapsulates business logic
- Controllers stay thin
- Services are reusable
- Easier to test
- Better separation of concerns

### Pattern: Repository Pattern (Light)
**Decision**: Use SQLAlchemy ORM directly (not full repository pattern)

**Rationale**:
- SQLAlchemy provides enough abstraction
- Simpler for small applications
- Less boilerplate code
- Can add repository layer later if needed

## Security Decisions

### Decision: Store Face Encodings, Not Images
**Rationale**:
- Privacy: Encodings cannot be reverse-engineered to images
- Storage: Encodings are much smaller (128 floats vs. MB images)
- Performance: Faster comparison
- Security: Less sensitive data to protect

**Trade-offs**:
- Cannot re-generate encodings from stored data
- Need to re-capture if algorithm changes

### Decision: Optional Face Recognition
**Rationale**:
- User choice and privacy
- Fallback to password always available
- Not all users have cameras
- Regulatory compliance (GDPR, CCPA)

### Decision: Confidence Threshold for Face Matching
**Rationale**:
- Balance security and usability
- Prevent false positives
- Configurable per deployment
- Industry best practice

**Default**: 0.6 (lower is stricter)

### Decision: Rate Limiting on Auth Endpoints
**Rationale**:
- Prevent brute force attacks
- Protect against DoS
- Industry standard practice

**Limits**:
- 5 failed attempts per 15 minutes per IP
- 10 successful logins per hour per user

## Data Flow Decisions

### Decision: Synchronous Face Processing
**Rationale**:
- Simpler implementation
- Face encoding is fast enough (<1 second)
- Real-time feedback to user
- No need for job queue

**Trade-offs**:
- Blocks request thread
- Not suitable for batch processing
- Can add async later if needed

### Decision: In-Memory Face Encoding Cache
**Rationale**:
- Faster face matching
- Reduce database queries
- Encodings are small
- Cache invalidation is simple

**Trade-offs**:
- Memory usage
- Need to handle cache invalidation
- Lost on server restart (acceptable)

## UI/UX Decisions

### Decision: Progressive Enhancement
**Rationale**:
- Works without JavaScript (basic functionality)
- Enhanced with JavaScript (better UX)
- Accessible to all users
- Graceful degradation

### Decision: Camera Preview Before Capture
**Rationale**:
- User can see what will be captured
- Better positioning
- Immediate feedback
- Industry standard (Zoom, Teams, etc.)

### Decision: Clear Error Messages
**Rationale**:
- Better user experience
- Reduces support burden
- Helps users self-serve
- Builds trust

## Scalability Decisions

### Decision: Stateless Backend
**Rationale**:
- Easy to scale horizontally
- No server affinity needed
- Can use load balancer
- Cloud-friendly

**Implementation**:
- Sessions in secure cookies (or Redis later)
- No in-memory state (except cache)

### Decision: Separate AI Service
**Rationale**:
- Can scale independently
- Can use GPU instances for AI service
- Can use cheaper instances for backend
- Can add multiple AI service instances

## Testing Decisions

### Decision: Unit Tests for Business Logic
**Rationale**:
- Fast feedback
- Easy to write
- High coverage possible
- Catches regressions

### Decision: Integration Tests for API
**Rationale**:
- Tests real behavior
- Catches integration issues
- Validates API contracts

### Decision: Manual Testing for Face Recognition
**Rationale**:
- Hard to automate camera interaction
- Need real faces for testing
- Visual verification needed
- Acceptable for MVP

## Deployment Decisions

### Decision: Environment-Based Configuration
**Rationale**:
- Different settings for dev/staging/prod
- Secrets not in code
- Easy to change without code changes
- Industry standard

### Decision: Docker-Ready (Future)
**Rationale**:
- Easy deployment
- Consistent environments
- Cloud-ready
- Can add later without major changes

## Future Considerations

### Potential Upgrades
1. **Database**: SQLite → PostgreSQL (for scale)
2. **Sessions**: Cookies → Redis (for distributed systems)
3. **AI Service**: Sync → Async (for batch processing)
4. **Frontend**: Server-side → React/Vue (for richer UX)
5. **Authentication**: Add OAuth (Google, GitHub)
6. **Face Recognition**: Add liveness detection (prevent photo attacks)
7. **Deployment**: Add Docker and Kubernetes support
8. **Monitoring**: Add logging, metrics, and alerting
9. **Testing**: Add E2E tests with Selenium/Playwright
10. **API**: Add GraphQL endpoint (if needed)
