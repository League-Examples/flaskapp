"""
Command 2 module for the Flask CLI.
"""
import click
from flask.cli import with_appcontext

@click.command('cmd2')
@with_appcontext
def cmd2_command():
    """Command 2: Prints 'command 2'."""
    click.echo('command 2')
