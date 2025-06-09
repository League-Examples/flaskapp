"""
Forms for the demo blueprint.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    """
    A simple form that accepts a name.
    """
    name = StringField('Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
