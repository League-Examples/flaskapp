import os
from .base import BaseConfig


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')
    
    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED = False
    
    # Testing-specific settings
    SERVER_NAME = 'localhost.localdomain'
