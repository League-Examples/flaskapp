"""
Config command module for the Flask CLI.
"""
import click
import os
from flask import current_app
from flask.cli import with_appcontext

@click.command('config')
@with_appcontext
def config_command():
    """
    Display configuration information.
    
    Prints out important environment variables and configuration settings:
    - FLASK_ENV: Current Flask environment
    - DATABASE_URI: Current database connection URI
    """
    # Get the current Flask environment
    flask_env = os.getenv('FLASK_ENV', 'development')
    click.echo(f"FLASK_ENV: {flask_env}")
    
    # Get the database URI from the application config
    database_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
    click.echo(f"DATABASE_URI: {database_uri}")
