"""Password reset controller."""
import logging
from flask import request, render_template, redirect, url_for, flash
from backend.app import db
from backend.models import User
from backend.services.email_service import EmailService
from backend.utils.response import success_response, error_response

logger = logging.getLogger(__name__)


class PasswordResetController:
    """Controller for password reset operations."""
    
    @staticmethod
    def request_reset():
        """
        Handle password reset request.
        
        POST /api/v1/auth/forgot-password
        Body: { "email": "user@example.com" }
        
        Returns:
            JSON response with success/error message
        """
        try:
            data = request.get_json()
            
            if not data or 'email' not in data:
                return error_response("Email is required", status_code=400)
            
            email = data['email'].strip().lower()
            
            # Validate email format
            is_valid, error_msg = User.validate_email(email)
            if not is_valid:
                return error_response(error_msg, status_code=400)
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            # SECURITY: Always return success even if user doesn't exist
            # This prevents email enumeration attacks
            if not user:
                logger.warning(f"Password reset requested for non-existent email: {email}")
                return success_response(
                    message="If an account exists with this email, you will receive a password reset link",
                    data=None
                )
            
            # Generate reset token
            reset_token = user.generate_reset_token()
            
            # Save token to database
            db.session.commit()
            
            # Send reset email
            success, error_msg = EmailService.send_password_reset_email(user, reset_token)
            
            if not success:
                logger.error(f"Failed to send reset email to {email}: {error_msg}")
                # Don't expose email sending failure to user
                return success_response(
                    message="If an account exists with this email, you will receive a password reset link",
                    data=None
                )
            
            logger.info(f"Password reset email sent to {email}")
            
            return success_response(
                message="If an account exists with this email, you will receive a password reset link",
                data=None
            )
            
        except Exception as e:
            logger.error(f"Error in request_reset: {str(e)}", exc_info=True)
            db.session.rollback()
            return error_response("An error occurred. Please try again later", status_code=500)
    
    @staticmethod
    def verify_reset_token(token):
        """
        Verify reset token and show reset password form.
        
        GET /auth/reset-password/<token>
        
        Returns:
            Rendered template or redirect
        """
        try:
            # Find user by token
            user = User.query.filter_by(reset_token=token).first()
            
            if not user:
                flash('Invalid or expired reset link', 'error')
                return redirect(url_for('auth.login'))
            
            # Verify token is not expired
            if not user.verify_reset_token(token):
                flash('This reset link has expired. Please request a new one', 'error')
                return redirect(url_for('auth.forgot_password'))
            
            # Show reset password form
            return render_template('reset_password.html', token=token)
            
        except Exception as e:
            logger.error(f"Error in verify_reset_token: {str(e)}", exc_info=True)
            flash('An error occurred. Please try again', 'error')
            return redirect(url_for('auth.login'))
    
    @staticmethod
    def reset_password(token):
        """
        Reset user password with new password.
        
        POST /auth/reset-password/<token>
        Body: { "password": "newpassword", "confirm_password": "newpassword" }
        
        Returns:
            Redirect to login page
        """
        try:
            data = request.form
            
            # Validate input
            if not data or 'password' not in data or 'confirm_password' not in data:
                flash('Password and confirmation are required', 'error')
                return redirect(url_for('auth.reset_password', token=token))
            
            password = data['password']
            confirm_password = data['confirm_password']
            
            # Check passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect(url_for('auth.reset_password', token=token))
            
            # Validate password strength
            is_valid, error_msg = User.validate_password(password)
            if not is_valid:
                flash(error_msg, 'error')
                return redirect(url_for('auth.reset_password', token=token))
            
            # Find user by token
            user = User.query.filter_by(reset_token=token).first()
            
            if not user:
                flash('Invalid or expired reset link', 'error')
                return redirect(url_for('auth.login'))
            
            # Verify token is not expired
            if not user.verify_reset_token(token):
                flash('This reset link has expired. Please request a new one', 'error')
                return redirect(url_for('auth.forgot_password'))
            
            # Update password
            user.set_password(password)
            
            # Clear reset token
            user.clear_reset_token()
            
            # Save changes
            db.session.commit()
            
            # Send confirmation email
            EmailService.send_password_changed_notification(user)
            
            logger.info(f"Password reset successful for user: {user.username}")
            
            flash('Your password has been reset successfully. Please login with your new password', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            logger.error(f"Error in reset_password: {str(e)}", exc_info=True)
            db.session.rollback()
            flash('An error occurred. Please try again', 'error')
            return redirect(url_for('auth.reset_password', token=token))
    
    @staticmethod
    def show_forgot_password_form():
        """
        Show forgot password form.
        
        GET /auth/forgot-password
        
        Returns:
            Rendered template
        """
        return render_template('forgot_password.html')
