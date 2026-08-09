"""Rate limiting middleware for face authentication."""
import logging
import time
from collections import defaultdict
from functools import wraps
from flask import request
from backend.utils import error_response

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter for face authentication."""
    
    def __init__(self):
        """Initialize rate limiter."""
        self.attempts = defaultdict(list)  # IP -> list of timestamps
        self.blocked = {}  # IP -> block_until_timestamp
    
    def is_blocked(self, ip):
        """Check if IP is currently blocked."""
        if ip in self.blocked:
            if time.time() < self.blocked[ip]:
                return True
            else:
                # Block expired, remove it
                del self.blocked[ip]
                return False
        return False
    
    def record_attempt(self, ip):
        """Record an authentication attempt."""
        current_time = time.time()
        
        # Clean old attempts (older than 5 minutes)
        self.attempts[ip] = [t for t in self.attempts[ip] if current_time - t < 300]
        
        # Add current attempt
        self.attempts[ip].append(current_time)
    
    def check_rate_limit(self, ip, max_attempts=5, window=60):
        """
        Check if IP has exceeded rate limit.
        
        Args:
            ip: IP address
            max_attempts: Maximum attempts allowed
            window: Time window in seconds
        
        Returns:
            Tuple of (is_allowed, remaining_attempts, retry_after)
        """
        current_time = time.time()
        
        # Check if blocked
        if self.is_blocked(ip):
            retry_after = int(self.blocked[ip] - current_time)
            logger.warning(f"Blocked IP {ip} attempted face login (blocked for {retry_after}s)")
            return False, 0, retry_after
        
        # Get recent attempts within window
        recent_attempts = [t for t in self.attempts.get(ip, []) if current_time - t < window]
        
        remaining = max_attempts - len(recent_attempts)
        
        if len(recent_attempts) >= max_attempts:
            # Block for 5 minutes
            block_duration = 300
            self.blocked[ip] = current_time + block_duration
            logger.warning(f"IP {ip} exceeded rate limit ({len(recent_attempts)} attempts in {window}s). Blocked for {block_duration}s")
            return False, 0, block_duration
        
        return True, remaining, 0
    
    def clear_attempts(self, ip):
        """Clear attempts for IP (called on successful login)."""
        if ip in self.attempts:
            del self.attempts[ip]
        if ip in self.blocked:
            del self.blocked[ip]


# Global rate limiter instance
face_auth_limiter = RateLimiter()


def rate_limit_face_auth(max_attempts=5, window=60):
    """
    Decorator for rate limiting face authentication.
    
    Args:
        max_attempts: Maximum attempts allowed (default: 5)
        window: Time window in seconds (default: 60)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get client IP
            ip = request.remote_addr
            
            # Check rate limit
            is_allowed, remaining, retry_after = face_auth_limiter.check_rate_limit(
                ip, max_attempts, window
            )
            
            if not is_allowed:
                logger.warning(f"Rate limit exceeded for IP {ip}")
                return error_response(
                    message='Too many authentication attempts',
                    error=f'Please wait {retry_after} seconds before trying again',
                    status_code=429
                )
            
            # Record attempt
            face_auth_limiter.record_attempt(ip)
            
            # Log remaining attempts
            if remaining <= 2:
                logger.warning(f"IP {ip} has {remaining} attempts remaining")
            
            # Call original function
            result = func(*args, **kwargs)
            
            # If authentication successful, clear attempts
            if result[1] == 200:  # Success status code
                face_auth_limiter.clear_attempts(ip)
                logger.info(f"Cleared rate limit for IP {ip} after successful authentication")
            
            return result
        
        return wrapper
    return decorator
