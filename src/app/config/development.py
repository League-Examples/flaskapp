import os
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    
    # SQLAlchemy database URI for development
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')
    
    # Additional development-specific settings
    LOG_LEVEL = 'DEBUG'
