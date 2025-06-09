"""
Command 1 module for the Flask CLI.
"""
import click
from flask.cli import with_appcontext

@click.command('cmd1')
@with_appcontext
def cmd1_command():
    """Command 1: Prints 'command 1'."""
    click.echo('command 1')
