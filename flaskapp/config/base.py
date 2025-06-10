import os
from pathlib import Path

# Get the base directory
basedir = Path(__file__).parent.parent.parent.parent


possible_oauth_providers = [
    'github',
    'google',
    'discord',
    'slack'
]

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
    
    # Session configuration
    SESSION_TYPE = 'sqlalchemy'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 604800  # 7 days in seconds
    
    # OAuth settings

    OAUTH_PROVIDERS = [ n for n in possible_oauth_providers 
                       if os.getenv(f'{n.upper()}_CLIENT_ID') and os.getenv(f'{n.upper()}_CLIENT_SECRET')]
    

   