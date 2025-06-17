"""
Models for authentication.
"""
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from flaskapp import db

class User(db.Model, UserMixin):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    display_name = db.Column(db.String(120), nullable=True)
    picture_url = db.Column(db.String(255), nullable=True)
    
    data = db.Column(db.JSON, nullable=True)

    # Relationships
    auth_providers = db.relationship('AuthProvider', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username or self.email}>'
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class AuthProvider(db.Model):
    """Model for authentication providers associated with users."""
    __tablename__ = 'auth_providers'
    
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(20), nullable=False)  # github, google, discord, slack
    provider_user_id = db.Column(db.String(255), nullable=False)
    
    # Provider-specific data
    access_token = db.Column(db.String(255), nullable=True)
    refresh_token = db.Column(db.String(255), nullable=True)
    token_expires_at = db.Column(db.Integer, nullable=True)
    
    # Provider profile data
    provider_username = db.Column(db.String(80), nullable=True)
    provider_email = db.Column(db.String(120), nullable=True)
    provider_picture = db.Column(db.String(255), nullable=True)
    
    # Relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='auth_providers')
    
    data = db.Column(db.JSON, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('provider', 'provider_user_id', name='unique_provider_user'),
    )
    
    def __repr__(self):
        return f'<AuthProvider {self.provider} - {self.provider_user_id}>'
