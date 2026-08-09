"""Frontend routes for serving HTML pages."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """Home page - redirect to login or dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    return redirect(url_for('frontend.login'))


@frontend_bp.route('/login')
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    return render_template('login.html')


@frontend_bp.route('/register')
def register():
    """Registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    return render_template('register.html')


@frontend_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page (requires authentication)."""
    return render_template('dashboard.html', user=current_user)


@frontend_bp.route('/settings')
@login_required
def settings():
    """Settings page (requires authentication)."""
    return render_template('settings.html', user=current_user)


@frontend_bp.route('/face/register')
@login_required
def face_register():
    """Face registration page (requires authentication)."""
    return render_template('face_register.html', user=current_user)


@frontend_bp.route('/face/login')
def face_login():
    """Face login page."""
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    return render_template('face_login.html')
