"""
Authentication package for Flask application.
This package provides authentication functionality using various providers.
"""
import os
from flask import Blueprint, url_for, request, session, redirect
from flask_login import LoginManager

# Create the login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

# Add this after your Blueprint definition



def init_app(app):
    """
    For the values of OAUTH_PROVIDERS, we check if the environment variables
    for the client ID and secret of each provider are set.  Then use the 
    flask-dance make_*_provider functions to create the OAuth providers.

    """

    # Initialize the login manager with the app
    login_manager.init_app(app)
    
    # Register the blueprint for authentication routes
    from .routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # construct the flask-dance providers

    for provider_name in app.config.get('OAUTH_PROVIDERS', []):

        client_id = os.getenv(f'{provider_name.upper()}_CLIENT_ID')
        client_secret = os.getenv(f'{provider_name.upper()}_CLIENT_SECRET')

        if provider_name == 'github':
            from flask_dance.contrib.github import make_github_blueprint
            github_bp = make_github_blueprint(
                client_id=client_id, client_secret=client_secret,
                redirect_to= "auth.github_authorized")
            
            app.register_blueprint(github_bp, url_prefix='/oauth/')
            app.github_bp = github_bp  # Store the blueprint for later use

        elif provider_name == 'google':
            from flask_dance.contrib.google import make_google_blueprint
            google_bp = make_google_blueprint(client_id=client_id, client_secret=client_secret, 
                scope=app.config.get('GOOGLE_LOGIN_SCOPES', 'openid'),
                reprompt_select_account=True,
                redirect_to="auth.google_authorized")

            app.register_blueprint(google_bp, url_prefix='/oauth/')
            app.google_bp = google_bp

        elif provider_name == 'discord':
            from flask_dance.contrib.discord import make_discord_blueprint
            discord_bp = make_discord_blueprint(client_id=client_id, client_secret=client_secret,
                redirect_to="auth.provider_authorized")
            app.register_blueprint(discord_bp, url_prefix='/oauth/')
            app.discord_bp = discord_bp

        elif provider_name == 'slack':
            from flask_dance.contrib.slack import make_slack_blueprint
            slack_bp = make_slack_blueprint(client_id=client_id, client_secret=client_secret,
                redirect_to="auth.slack_authorized")
            app.register_blueprint(slack_bp, url_prefix='/oauth/slack')
            app.slack_bp = slack_bp




# Import routes to avoid circular imports
from . import routes
from .routes import auth_bp
