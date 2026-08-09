"""Centralized logging configuration."""
import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """Configure application logging."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_level = logging.DEBUG if app.debug else logging.INFO

    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    audit_formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Main rotating file handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'faceauth.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)

    # Error-only file handler
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # Dedicated face-auth audit log
    audit_handler = RotatingFileHandler(
        os.path.join(log_dir, 'face_auth_audit.log'),
        maxBytes=10 * 1024 * 1024, backupCount=10
    )
    audit_handler.setLevel(logging.INFO)
    audit_handler.setFormatter(audit_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    # App logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)

    # Dedicated audit logger (face_auth.audit)
    audit_log = logging.getLogger('face_auth.audit')
    audit_log.setLevel(logging.INFO)
    audit_log.addHandler(audit_handler)
    audit_log.addHandler(console_handler)
    audit_log.propagate = False   # don't double-log to root

    # Suppress noisy loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    app.logger.info('=' * 50)
    app.logger.info('Face Authentication System - Logging Initialized')
    app.logger.info(f'Log Level: {logging.getLevelName(log_level)}')
    app.logger.info(f'Log Directory: {os.path.abspath(log_dir)}')
    app.logger.info('Audit log: logs/face_auth_audit.log')
    app.logger.info('=' * 50)
