"""
Authentication package for Flask application.
This package provides authentication functionality using various providers.
"""
import os
from flask import Blueprint
from flask_login import LoginManager

# Create the login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


# Import routes to avoid circular imports
from . import routes
from .routes import auth_bp
