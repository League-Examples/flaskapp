"""
Routes for the demo blueprint.
"""
from flask import render_template, flash, redirect, url_for
from flaskapp.demo import demo_bp
from flaskapp.demo.forms import NameForm

@demo_bp.route('/')
def index():
    """
    Demo index page that lists other demo pages.
    """
    return render_template('demo/index.html', title='Demo Index')

@demo_bp.route('/hello')
def hello():
    """
    A simple page that says hello and displays the flag.png image.
    """
    return render_template('demo/hello.html', title='Hello')

@demo_bp.route('/form', methods=['GET', 'POST'])
def form():
    """
    A form that accepts a name and displays a greeting.
    """
    form = NameForm()
    greeting = None
    if form.validate_on_submit():
        greeting = f"Hello, {form.name.data}!"
        flash(f'Hello, {form.name.data}!', 'success')
    return render_template('demo/form.html', title='Form Demo', form=form, greeting=greeting)
