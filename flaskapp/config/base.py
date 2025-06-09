import os
from pathlib import Path

# Get the base directory
basedir = Path(__file__).parent.parent.parent.parent


class BaseConfig:
    """Base configuration class with settings common to all environments."""
    
    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    DEBUG = False
    TESTING = False
    
    # Static and template folder settings
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
