import os
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    
    # Database settings for development with Docker PostgreSQL
    DB_USER = os.getenv('DEV_DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DEV_DB_NAME', 'flaskapp_dev')
    DB_HOST = os.getenv('DEV_DB_HOST', 'localhost')
    DB_PORT = os.getenv('DEV_DB_PORT', '5432')

    from_parts = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # SQLAlchemy database URI for development
    # Default to SQLite but can easily switch to PostgreSQL with Docker
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', from_parts)

    
    # Additional development-specific settings
    LOG_LEVEL = 'DEBUG'

 