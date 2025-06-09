"""
Development CLI commands for the Flask application.
"""
import click
from flask.cli import AppGroup, with_appcontext
import subprocess
import os
import time

# Create a dev command group
dev_cli = AppGroup('dev', help='Development commands')

# Create a db subcommand group
db_cli = AppGroup('db', help='Database management commands')
dev_cli.add_command(db_cli)

@db_cli.command('start')
@with_appcontext
def db_start():
    """Start the PostgreSQL database in Docker."""
    from flask import current_app
    
    click.echo("Starting PostgreSQL database in Docker...")
    
    # Get database credentials from config
    user = current_app.config.get('DB_USER', 'postgres')
    password = current_app.config.get('DB_PASSWORD', 'postgres')
    db_name = current_app.config.get('DB_NAME', 'flaskapp_dev')
    port = current_app.config.get('DB_PORT', 5432)
    
    # Run the Docker command to start PostgreSQL
    cmd = [
        "docker", "run", "--name", "flaskapp_dev_db", "-d",
        "-e", f"POSTGRES_USER={user}",
        "-e", f"POSTGRES_PASSWORD={password}",
        "-e", f"POSTGRES_DB={db_name}",
        "-p", f"{port}:5432",
        "postgres:16-alpine"
    ]
    
    try:
        # Check if container already exists
        container_check = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=flaskapp_dev_db", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        
        if "flaskapp_dev_db" in container_check.stdout:
            # Container exists, check if it's running
            status_check = subprocess.run(
                ["docker", "ps", "--filter", "name=flaskapp_dev_db", "--format", "{{.Names}}"],
                capture_output=True, text=True
            )
            
            if "flaskapp_dev_db" in status_check.stdout:
                click.echo("Database is already running.")
                return
            
            # Container exists but not running, start it
            subprocess.run(["docker", "start", "flaskapp_dev_db"], check=True)
            click.echo("Started existing database container.")
        else:
            # Container doesn't exist, create and start it
            subprocess.run(cmd, check=True)
            click.echo("Created and started new database container.")
        
        # Wait a moment for the database to be ready
        click.echo("Waiting for database to be ready...")
        time.sleep(3)
        
        click.echo(f"Database is running!")
        click.echo(f"Connection details:")
        click.echo(f"  Host: localhost")
        click.echo(f"  Port: {port}")
        click.echo(f"  User: {user}")
        click.echo(f"  Password: {password}")
        click.echo(f"  Database: {db_name}")
        click.echo(f"  URI: postgresql://{user}:{password}@localhost:{port}/{db_name}")
        
    except subprocess.CalledProcessError as e:
        click.echo(f"Error starting database: {e}", err=True)
        raise click.Abort()

@db_cli.command('stop')
@with_appcontext
def db_stop():
    """Stop the PostgreSQL database in Docker."""
    click.echo("Stopping PostgreSQL database in Docker...")
    
    try:
        # Check if container exists
        container_check = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=flaskapp_dev_db", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        
        if "flaskapp_dev_db" not in container_check.stdout:
            click.echo("Database container does not exist.")
            return
        
        # Stop the container
        subprocess.run(["docker", "stop", "flaskapp_dev_db"], check=True)
        click.echo("Database stopped.")
        
    except subprocess.CalledProcessError as e:
        click.echo(f"Error stopping database: {e}", err=True)
        raise click.Abort()

@db_cli.command('status')
def db_status():
    """Check the status of the PostgreSQL database in Docker."""
    click.echo("Checking PostgreSQL database status...")
    
    try:
        # Check if container exists and is running
        container_check = subprocess.run(
            ["docker", "ps", "--filter", "name=flaskapp_dev_db", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        
        if "flaskapp_dev_db" in container_check.stdout:
            click.echo("Database is running.")
            
            # Get the port mapping
            port_check = subprocess.run(
                ["docker", "port", "flaskapp_dev_db", "5432"],
                capture_output=True, text=True
            )
            
            if port_check.stdout:
                click.echo(f"Port mapping: {port_check.stdout.strip()}")
            
            return True
        else:
            # Check if it exists but is stopped
            container_check = subprocess.run(
                ["docker", "ps", "-a", "--filter", "name=flaskapp_dev_db", "--format", "{{.Names}}"],
                capture_output=True, text=True
            )
            
            if "flaskapp_dev_db" in container_check.stdout:
                click.echo("Database container exists but is not running.")
            else:
                click.echo("Database container does not exist.")
                
            return False
            
    except subprocess.CalledProcessError as e:
        click.echo(f"Error checking database status: {e}", err=True)
        raise click.Abort()
