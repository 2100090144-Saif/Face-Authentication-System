"""User model."""
from datetime import datetime
from flask_login import UserMixin
from backend.app import db, bcrypt


class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    face_recognition_enabled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Password reset fields
    reset_token = db.Column(db.String(100), unique=True, nullable=True, index=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    face_encodings = db.relationship('FaceEncoding', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (exclude sensitive data)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'face_recognition_enabled': self.face_recognition_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def validate_username(username):
        """Validate username format."""
        if not username or len(username) < 3 or len(username) > 80:
            return False, "Username must be between 3 and 80 characters"
        if not username.replace('_', '').isalnum():
            return False, "Username can only contain letters, numbers, and underscores"
        return True, None
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        if not email or '@' not in email or '.' not in email:
            return False, "Invalid email format"
        if len(email) > 120:
            return False, "Email too long"
        return True, None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength."""
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters"
        return True, None
    
    def generate_reset_token(self):
        """Generate a secure password reset token."""
        import secrets
        self.reset_token = secrets.token_urlsafe(32)
        # Token expires in 1 hour
        from datetime import timedelta
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify if reset token is valid and not expired."""
        if not self.reset_token or not self.reset_token_expiry:
            return False
        if self.reset_token != token:
            return False
        if datetime.utcnow() > self.reset_token_expiry:
            return False
        return True
    
    def clear_reset_token(self):
        """Clear reset token after use."""
        self.reset_token = None
        self.reset_token_expiry = None
