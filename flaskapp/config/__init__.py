import os
from flask import Flask

# Import config classes
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

# Dictionary with different configuration environments
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def configure_app(app: Flask):
    """Configure the app with the appropriate config class based on environment."""
    config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config_dict[config_name])
