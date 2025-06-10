"""
Authentication package for Flask application.
This package provides authentication functionality using various providers.
"""
import os
from flask import Blueprint
from flask_login import LoginManager
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.discord import make_discord_blueprint
from flask_dance.contrib.slack import make_slack_blueprint

# Create the login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Main auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth', 
                    template_folder='templates')

# Create a dict to store provider blueprints
provider_blueprints = {}

# Import routes to avoid circular imports
from . import routes

def init_app(app):
    """Initialize authentication for the application."""
    # Configure login manager
    login_manager.init_app(app)
    
    # Import User model here to avoid circular imports
    from .models import User, AuthProvider
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID."""
        return User.query.get(int(user_id))
    
    # Register OAuth providers based on environment variables
    providers = ['github', 'google', 'discord', 'slack']
    registered_providers = []
    
    for provider in providers:
        client_id = os.environ.get(f'{provider.upper()}_CLIENT_ID')
        client_secret = os.environ.get(f'{provider.upper()}_CLIENT_SECRET')
        
        if client_id and client_secret:
            provider_bp = register_oauth_provider(provider, client_id, client_secret, app)
            if provider_bp:
                registered_providers.append(provider)
    
    # Store the list of registered providers in app config for templates
    app.config['OAUTH_PROVIDERS'] = registered_providers
    
    # Register the main auth blueprint
    app.register_blueprint(auth_bp)

def register_oauth_provider(provider, client_id, client_secret, app):
    """Register an OAuth provider using Flask-Dance."""
    from .models import AuthProvider
    
    # Common configuration
    redirect_url = f'/auth/{provider}/authorized'
    storage = SQLAlchemyStorage(AuthProvider, app.extensions['sqlalchemy'].db, user=None, provider=provider)
    
    # Create blueprint based on provider
    if provider == 'github':
        bp = make_github_blueprint(
            client_id=client_id,
            client_secret=client_secret,
            scope='user:email',
            redirect_url=redirect_url,
            storage=storage
        )
    elif provider == 'google':
        bp = make_google_blueprint(
            client_id=client_id,
            client_secret=client_secret,
            scope=['profile', 'email'],
            redirect_url=redirect_url,
            storage=storage
        )
    elif provider == 'discord':
        # Create custom Discord blueprint since Flask-Dance doesn't have discord built-in
        bp = OAuth2ConsumerBlueprint(
            f"{provider}",
            __name__,
            client_id=client_id,
            client_secret=client_secret,
            base_url="https://discord.com/api/",
            token_url="https://discord.com/api/oauth2/token",
            authorization_url="https://discord.com/api/oauth2/authorize",
            scope=["identify", "email"],
            redirect_url=redirect_url,
            storage=storage
        )
    elif provider == 'slack':
        # Create custom Slack blueprint since Flask-Dance doesn't have slack built-in
        bp = OAuth2ConsumerBlueprint(
            f"{provider}",
            __name__,
            client_id=client_id,
            client_secret=client_secret,
            base_url="https://slack.com/api/",
            token_url="https://slack.com/api/oauth.v2.access",
            authorization_url="https://slack.com/oauth/v2/authorize",
            scope=["identity.basic", "identity.email"],
            redirect_url=redirect_url,
            storage=storage
        )
    else:
        return None
    
    # Register the provider blueprint with URL prefix
    bp.url_prefix = f"/auth/{provider}"
    app.register_blueprint(bp)
    
    # Store the blueprint reference
    provider_blueprints[provider] = bp
    
    return bp
