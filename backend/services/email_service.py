"""Email service for sending notifications."""
import logging
from flask import current_app, url_for
from flask_mail import Message
from backend.app import mail

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails."""
    
    @staticmethod
    def send_password_reset_email(user, reset_token):
        """
        Send password reset email to user.
        
        Args:
            user: User object
            reset_token: Password reset token
            
        Returns:
            Tuple of (success: bool, error_message: str or None)
        """
        try:
            # Generate reset URL
            reset_url = url_for('auth_routes.reset_password', 
                              token=reset_token, 
                              _external=True)
            
            # Create email message
            msg = Message(
                subject='Password Reset Request - Face Authentication System',
                recipients=[user.email],
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@faceauth.com')
            )
            
            # Email body (plain text)
            msg.body = f"""
Hello {user.username},

You have requested to reset your password for Face Authentication System.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.

Best regards,
Face Authentication System Team
"""
            
            # Email body (HTML)
            msg.html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Password Reset Request</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user.username}</strong>,</p>
            
            <p>You have requested to reset your password for Face Authentication System.</p>
            
            <p>Click the button below to reset your password:</p>
            
            <p style="text-align: center;">
                <a href="{reset_url}" class="button">Reset Password</a>
            </p>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f0f0f0; padding: 10px; border-radius: 3px;">
                {reset_url}
            </p>
            
            <div class="warning">
                <strong>⚠️ Important:</strong>
                <ul>
                    <li>This link will expire in <strong>1 hour</strong></li>
                    <li>If you did not request this reset, please ignore this email</li>
                    <li>Your password will not change until you create a new one</li>
                </ul>
            </div>
        </div>
        <div class="footer">
            <p>Face Authentication System</p>
            <p>This is an automated email. Please do not reply.</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Send email
            mail.send(msg)
            
            logger.info(f"Password reset email sent to {user.email}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to send password reset email: {str(e)}", exc_info=True)
            return False, "Failed to send email. Please try again later."
    
    @staticmethod
    def send_password_changed_notification(user):
        """
        Send notification email when password is changed.
        
        Args:
            user: User object
            
        Returns:
            Tuple of (success: bool, error_message: str or None)
        """
        try:
            msg = Message(
                subject='Password Changed - Face Authentication System',
                recipients=[user.email],
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@faceauth.com')
            )
            
            msg.body = f"""
Hello {user.username},

Your password has been successfully changed.

If you did not make this change, please contact support immediately.

Best regards,
Face Authentication System Team
"""
            
            msg.html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }}
        .alert {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Password Changed</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user.username}</strong>,</p>
            
            <div class="alert">
                <strong>✅ Success!</strong><br>
                Your password has been successfully changed.
            </div>
            
            <p>If you made this change, no further action is required.</p>
            
            <div class="warning">
                <strong>⚠️ Didn't make this change?</strong><br>
                If you did not change your password, your account may be compromised.
                Please contact support immediately.
            </div>
        </div>
    </div>
</body>
</html>
"""
            
            mail.send(msg)
            logger.info(f"Password changed notification sent to {user.email}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to send password changed notification: {str(e)}", exc_info=True)
            return False, "Failed to send notification email"
