"""
Flask application factory module.
This module contains the application factory function that creates and configures
the Flask application instance.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_font_awesome import FontAwesome
from flask_login import current_user
from flask_migrate import Migrate
from importlib.metadata import metadata, version

# Initialize extensions
db = SQLAlchemy()
bootstrap = Bootstrap5()
fa = FontAwesome()
migrate = Migrate()

class FlaskApp(Flask):
    """
    Flask application factory implemented as a class.
    Creates and configures an instance of the Flask application.
    """
    
    def __init__(self, import_name=__name__, template_folder='templates', **kwargs):
        """Initialize the Flask app with the given parameters"""
        super().__init__(import_name, template_folder=template_folder, **kwargs)
        
        # Determine the configuration to use
        self._configure_app()
        
        # Initialize extensions
        self._init_extensions()
        
        # Register blueprints
        self._register_blueprints()
        
        # Register CLI commands
        self._register_cli_commands()
        
        # Create database tables
        self._create_database()
        
        # Register context processors
        self._register_context_processors()
    
    def _configure_app(self):
        """Configure the Flask application"""
        config_name = os.getenv('FLASK_ENV', 'development')
        
        # Load the appropriate configuration
        if config_name == 'production':
            self.config.from_object('flaskapp.config.production.ProductionConfig')
        elif config_name == 'testing':
            self.config.from_object('flaskapp.config.testing.TestingConfig')
        else:
            self.config.from_object('flaskapp.config.development.DevelopmentConfig')
        
        # Allow OAuth over http in debug mode for development
        if self.debug or os.environ.get('FLASK_ENV') == 'development':
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    def _init_extensions(self):
        """Initialize Flask extensions"""
        db.init_app(self)
        bootstrap.init_app(self)
        fa.init_app(self)
        migrate.init_app(self, db)
    
    def _register_blueprints(self):
        """Register all blueprints with the app"""
        from flaskapp.main.routes import main_bp
        self.register_blueprint(main_bp)
        
        from flaskapp.demo import demo_bp
        self.register_blueprint(demo_bp)
        
        import flaskapp.auth
        flaskapp.auth.init_app(self)
    
    def _register_cli_commands(self):
        """Register CLI commands with the application"""
        # Import CLI commands

        from flaskapp.cli.config import config_command
        from flaskapp.cli.dev import dev_cli
        
        # Add commands to the Flask CLI

        self.cli.add_command(config_command)
        self.cli.add_command(dev_cli)
    
    def _create_database(self):
        """Create database tables"""
        from flaskapp.auth.models import User, AuthProvider

        with self.app_context():
            db.create_all()
    
    def _register_context_processors(self):
        """Register context processors"""
        @self.context_processor
        def inject_common_variables():
            """
            Inject common variables into the template context.
            """
            meta = metadata("flaskapp")
            
            return {
                "current_user": current_user,
                'meta': {
                    "site_name": meta["Name"],
                    "version": version(meta["Name"]), 
                }
            }
