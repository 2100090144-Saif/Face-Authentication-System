# 📁 Project Structure

This document explains the clean, production-ready architecture of the Face Authentication System.

## 🏗️ Directory Layout

```
app/
├── .kiro/
│   └── steering/              # Auto-read development guidelines (Kiro IDE)
│       ├── best_practices.md
│       ├── dos_and_donts.md
│       └── rules.md
│
├── frontend/                  # Frontend assets
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Main stylesheet
│   │   └── js/
│   │       ├── auth.js       # Authentication JS
│   │       ├── face_login.js # Face login functionality
│   │       ├── face_register.js
│   │       ├── main.js       # Common utilities
│   │       └── settings.js   # Settings page JS
│   └── templates/             # Jinja2 HTML templates
│       ├── base.html         # Base template
│       ├── dashboard.html
│       ├── face_login.html
│       ├── face_register.html
│       ├── login.html
│       ├── register.html
│       └── settings.html
│
├── backend/                   # Flask backend (MVC pattern)
│   ├── app.py                # Flask app factory
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Environment-based config
│   ├── models/               # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── face_encoding.py # Face encoding model
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Authentication logic
│   │   └── face_service.py  # Face recognition logic
│   ├── controllers/          # Request handlers
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── face_controller.py
│   │   └── settings_controller.py
│   ├── routes/               # URL routing
│   │   ├── __init__.py
│   │   ├── auth_routes.py   # /api/v1/auth/*
│   │   ├── face_routes.py   # /api/v1/face/*
│   │   ├── settings_routes.py
│   │   └── frontend_routes.py # HTML page routes
│   ├── middleware/           # Custom middleware
│   │   └── __init__.py
│   └── utils/                # Utilities
│       ├── __init__.py
│       ├── extensions.py    # Flask extensions
│       ├── logger.py        # Logging config
│       └── response.py      # Standardized responses
│
├── ai_service/               # AI/ML service (decoupled)
│   ├── __init__.py
│   ├── face_detection.py    # Haarcascade face detection
│   ├── face_recognition.py  # dlib face recognition
│   ├── utils.py             # Image processing utilities
│   ├── models/              # ML models
│   │   └── haarcascade_frontalface_default.xml
│   └── data/                # Face data storage
│       └── (user face images - optional)
│
├── architecture/             # Architecture documentation
│   ├── api.md               # API documentation
│   ├── decisions.md         # Architecture Decision Records
│   ├── flow.md              # Application flow diagrams
│   ├── models.md            # Data models documentation
│   └── plans.md             # Implementation plans
│
├── suggestions/              # Improvement suggestions
│   ├── performance/
│   │   └── improvements.md
│   ├── scalability/
│   │   └── improvements.md
│   ├── security/
│   │   └── improvements.md
│   └── ux/
│       └── improvements.md
│
├── instance/                 # Instance-specific files (gitignored)
│   └── app.db               # SQLite database
│
├── .env                      # Environment variables (gitignored)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── run.py                    # ⭐ SINGLE ENTRY POINT
├── README.md                 # Main documentation
└── PROJECT_STRUCTURE.md      # This file
```

## 🎯 Design Principles

### 1. Single Entry Point
- **`run.py`** is the ONLY way to start the application
- No confusion with multiple entry points
- Loads `.env` automatically
- Configurable via environment variables

### 2. Separation of Concerns
- **Frontend**: HTML templates + static assets (CSS/JS)
- **Backend**: Flask app following MVC pattern
- **AI Service**: Completely decoupled face recognition logic

### 3. MVC Pattern (Backend)
```
Request → Route → Controller → Service → Model → Database
                      ↓
                  Response
```

- **Routes**: Define URL endpoints
- **Controllers**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Models**: Database schema and ORM

### 4. Configuration Management
- All settings in `.env` file
- Environment-based configs (dev/prod/test)
- Single source of truth

### 5. Modular AI Service
- Independent from Flask
- Can be extracted as microservice
- Uses standard interfaces

## 📂 Key Files Explained

### Entry Point
- **`run.py`**: Starts the Flask server with config from `.env`

### Backend Core
- **`backend/app.py`**: Flask application factory
- **`backend/config/settings.py`**: Configuration classes
- **`backend/models/user.py`**: User database model
- **`backend/services/auth_service.py`**: Authentication business logic
- **`backend/controllers/auth_controller.py`**: Auth request handlers
- **`backend/routes/auth_routes.py`**: Auth URL routing

### AI Service
- **`ai_service/face_detection.py`**: OpenCV Haarcascade face detection
- **`ai_service/face_recognition.py`**: dlib face encoding & matching
- **`ai_service/utils.py`**: Image processing helpers

### Frontend
- **`frontend/templates/base.html`**: Base template with navigation
- **`frontend/static/css/style.css`**: Main stylesheet
- **`frontend/static/js/main.js`**: Common JavaScript utilities

## 🔄 Data Flow

### User Registration
```
Browser → POST /api/v1/auth/register
       → AuthController.register()
       → AuthService.register_user()
       → User.create()
       → Database
```

### Face Login
```
Browser → POST /api/v1/face/login (with image)
       → FaceController.login_face()
       → FaceService.authenticate_face()
       → FaceRecognizer.generate_encoding()
       → FaceRecognizer.find_best_match()
       → User.query (find matching user)
       → Flask-Login (create session)
```

## 🚀 Running the Application

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment (optional - has defaults)
cp .env.example .env
# Edit .env if needed

# 3. Run the application
python run.py

# 4. Open browser
# https://127.0.0.1:5000
```

## 📝 Adding New Features

### Add a new API endpoint:
1. Create service method in `backend/services/`
2. Create controller method in `backend/controllers/`
3. Add route in `backend/routes/`
4. Register blueprint in `backend/routes/__init__.py`

### Add a new page:
1. Create HTML template in `frontend/templates/`
2. Add route in `backend/routes/frontend_routes.py`
3. Add JavaScript in `frontend/static/js/` if needed

### Add AI functionality:
1. Add function in `ai_service/`
2. Call from `backend/services/face_service.py`
3. Never import AI service directly in controllers

## 🔒 Security Notes

- `.env` is gitignored (never commit secrets)
- `instance/` is gitignored (database not in repo)
- Passwords hashed with bcrypt
- Face encodings stored (not raw images)
- HTTPS enabled by default (self-signed cert for dev)

## 📚 Documentation

- **README.md**: User-facing documentation
- **architecture/**: Technical architecture docs
- **suggestions/**: Improvement ideas
- **.kiro/steering/**: Development guidelines (auto-read by Kiro IDE)

## ✅ What Was Cleaned Up

### Removed Duplicates:
- ❌ `ai-service/` (kept `ai_service/`)
- ❌ `steering/` (kept `.kiro/steering/`)
- ❌ `models/` in root (kept in `ai_service/models/`)
- ❌ `templates/` in root (kept in `frontend/templates/`)

### Removed Old Files:
- ❌ `app.py` (root)
- ❌ `auth.py` (root)
- ❌ `register.py` (root)
- ❌ `captured.jpg`
- ❌ Old documentation files

### Moved Files:
- ✅ `dataset/` → `ai_service/data/`
- ✅ Templates consolidated in `frontend/templates/`

## 🎓 Best Practices

1. **Never modify `run.py`** - configure via `.env` instead
2. **Keep services thin** - delegate to models
3. **Keep controllers thin** - delegate to services
4. **AI service is independent** - no Flask imports
5. **Use environment variables** - never hardcode config
6. **Follow the MVC pattern** - maintain separation

---

**This structure is production-ready, scalable, and maintainable.**
