# Face Authentication System

A modern, production-ready face authentication system with user management, password-based login, and optional face recognition.

## Features

- **User Authentication**
  - Traditional username/password login
  - Secure password hashing with bcrypt
  - Session management with Flask-Login
  - User registration and profile management

- **Face Recognition**
  - Optional face-based login
  - Face encoding storage (privacy-friendly)
  - High-accuracy face matching using dlib
  - Enable/disable per user

- **Modern UI**
  - Responsive design
  - Clean, intuitive interface
  - Real-time camera preview
  - Clear error messages and feedback

- **Security**
  - Password hashing
  - Secure session management
  - Input validation
  - CSRF protection ready

## Architecture

```
app/
├── frontend/          # HTML templates and static files
│   ├── templates/     # Jinja2 templates
│   └── static/        # CSS, JavaScript, images
├── backend/           # Flask application
│   ├── routes/        # API and frontend routes
│   ├── controllers/   # Request handlers
│   ├── services/      # Business logic
│   ├── models/        # Database models
│   └── config/        # Configuration
├── ai-service/        # Face detection and recognition
│   ├── face_detection.py
│   ├── face_recognition.py
│   └── utils.py
├── architecture/      # Architecture documentation
├── suggestions/       # Improvement suggestions
└── steering/          # Development guidelines
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip
- Webcam (for face recognition)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Installing `dlib` may require additional system dependencies:
   
   - **Windows**: Install Visual Studio Build Tools
   - **Linux**: `sudo apt-get install build-essential cmake`
   - **Mac**: `brew install cmake`

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Registration

1. Navigate to `/register`
2. Fill in username, email, and password
3. Click "Register"
4. You'll be automatically logged in

### Password Login

1. Navigate to `/login`
2. Enter username and password
3. Click "Login"

### Enable Face Recognition

1. Login to your account
2. Go to Settings
3. Toggle "Face Recognition" on
4. Click "Register Your Face"
5. Allow camera access
6. Position your face in the frame
7. Click "Capture & Register"

### Face Login

1. Navigate to `/login`
2. Click "Face Recognition" tab
3. Click "Start Face Login"
4. Allow camera access
5. Position your face in the frame
6. Click "Authenticate"

## API Documentation

See [architecture/api.md](architecture/api.md) for complete API documentation.

### Key Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with password
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/face/register` - Register face
- `POST /api/v1/face/login` - Login with face
- `GET /api/v1/settings` - Get user settings
- `PUT /api/v1/settings/face-recognition` - Toggle face recognition

## Configuration

Edit `.env` file to configure:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///app.db

# Face Recognition
FACE_RECOGNITION_TOLERANCE=0.6  # Lower is stricter (0.0-1.0)
FACE_ENCODING_MODEL=large       # 'small' or 'large'
```

## Development

### Project Structure

- **Frontend**: HTML templates with vanilla JavaScript
- **Backend**: Flask with MVC pattern
- **AI Service**: Separate module for face operations
- **Database**: SQLite (easily upgradable to PostgreSQL)

### Adding Features

1. Create model in `backend/models/`
2. Create service in `backend/services/`
3. Create controller in `backend/controllers/`
4. Create routes in `backend/routes/`
5. Create templates in `frontend/templates/`
6. Add JavaScript in `frontend/static/js/`

### Testing

```bash
# Run tests (when implemented)
pytest

# Check code style
flake8 backend/ ai-service/
```

## Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY` in environment
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set `FLASK_ENV=production`
- [ ] Configure proper logging
- [ ] Set up monitoring
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use production WSGI server (gunicorn)

### Docker Deployment (Future)

```bash
docker build -t face-auth .
docker run -p 5000:5000 face-auth 
```

## Security Considerations

- Passwords are hashed with bcrypt
- Face encodings cannot be reverse-engineered to images
- Sessions are secure and HTTP-only
- Input validation on all endpoints
- CSRF protection ready
- Rate limiting recommended for production

## Troubleshooting

### Camera not working

- Check browser permissions
- Ensure HTTPS (required for camera in production)
- Try different browser

### Face not detected

- Ensure good lighting
- Face camera directly
- Remove glasses if possible
- Check camera quality

### Installation issues

- **dlib fails to install**: Install build tools (see Prerequisites)
- **OpenCV issues**: Try `pip install opencv-python-headless`
- **Permission errors**: Use virtual environment

## Future Enhancements

See [suggestions/](suggestions/) directory for detailed improvement suggestions:

- Liveness detection (prevent photo attacks)
- Multi-factor authentication
- OAuth integration (Google, GitHub)
- Mobile app
- Admin dashboard
- Analytics and logging
- Docker support
- Kubernetes deployment

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## Support

For issues and questions:
- Check [architecture/](architecture/) for documentation
- Review [suggestions/](suggestions/) for known improvements
- Open an issue on GitHub

## Credits

- Face recognition powered by [face_recognition](https://github.com/ageitgey/face_recognition)
- Face detection using OpenCV Haar Cascades
- Built with Flask and modern web technologies
