import os
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    
    DEBUG = False
    
    # Database URI must be set in environment variables for production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    
    # Additional production-specific settings
    LOG_LEVEL = 'ERROR'
    
    # Enable CSRF protection in production
    WTF_CSRF_ENABLED = True
