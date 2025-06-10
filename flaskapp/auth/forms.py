"""
Forms for authentication.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class ProfileForm(FlaskForm):
    """Form for editing user profile."""
    username = StringField('Username', validators=[Length(min=3, max=80)])
    display_name = StringField('Display Name', validators=[Length(max=120)])
    email = StringField('Email', validators=[Email(), Length(max=120)])
    submit = SubmitField('Update Profile')