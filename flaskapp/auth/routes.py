from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import oauth
from .models import User, AuthProvider
from flaskapp import db
from .forms import ProfileForm
import time
import json

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth',
                   template_folder='templates')

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """Login route showing available authentication providers."""
    # If user is already logged in, redirect to index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Get the next URL from the query string
    next_url = request.args.get('next')
    if next_url:
        session['next_url'] = next_url
    
    # Get the list of registered providers
    providers = current_app.config.get('OAUTH_PROVIDERS', [])
    
    return render_template('auth/login.html', providers=providers)

@auth_bp.route('/logout/')
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/link/')
@login_required
def link():
    """Link accounts page."""
    # Get the list of registered providers
    providers = current_app.config.get('OAUTH_PROVIDERS', [])
    
    # Get the list of providers that the user has already linked
    linked_providers = [provider.provider for provider in current_user.auth_providers]
    
    return render_template('auth/link.html', 
                          providers=providers, 
                          linked_providers=linked_providers)

@auth_bp.route('/unlink/<provider>')
@login_required
def unlink(provider):
    """Unlink a provider from the user account."""
    # Check if the user has more than one provider linked
    if len(current_user.auth_providers) <= 1:
        flash('You must have at least one authentication method linked.', 'danger')
        return redirect(url_for('auth.link'))
    
    # Find the provider to unlink
    auth_provider = AuthProvider.query.filter_by(
        user_id=current_user.id, 
        provider=provider
    ).first()
    
    if auth_provider:
        db.session.delete(auth_provider)
        db.session.commit()
        flash(f'Your {provider.capitalize()} account has been unlinked.', 'success')
    else:
        flash(f'Provider {provider} not found.', 'danger')
    
    return redirect(url_for('auth.link'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page."""
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.display_name = form.display_name.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    
    # Pre-populate the form with current user data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.display_name.data = current_user.display_name
    
    return render_template('auth/profile.html', form=form)

# OAuth routes for each provider
@auth_bp.route('/<provider>/login')
def provider_login(provider):
    """Redirect to provider authorization page."""
    # Store original url in session for callback
    redirect_uri = url_for('auth.provider_authorized', provider=provider, _external=True)
    
    # For linking accounts, check if user is already logged in
    is_linking = current_user.is_authenticated
    if is_linking:
        session['linking'] = True
    
    return oauth.create_client(provider).authorize_redirect(redirect_uri)

@auth_bp.route('/<provider>/authorized')
def provider_authorized(provider):
    """Callback route after provider authorization."""
    token = oauth.create_client(provider).authorize_access_token()
    
    # Get user info from provider
    provider_user_info = get_provider_user_info(provider, token)
    
    if not provider_user_info:
        flash('Failed to get user info from provider.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Check if this is a linking operation
    is_linking = session.pop('linking', False)
    
    # Find if this provider account is already registered
    auth_provider = AuthProvider.query.filter_by(
        provider=provider, 
        provider_user_id=provider_user_info['id']
    ).first()
    
    if auth_provider:
        # Provider account already exists
        if is_linking:
            if auth_provider.user_id == current_user.id:
                flash(f'This {provider.capitalize()} account is already linked to your account.', 'info')
            else:
                flash(f'This {provider.capitalize()} account is already linked to another account.', 'danger')
            return redirect(url_for('auth.link'))
        
        # Login case - log in the user
        login_user(auth_provider.user)
        flash(f'Logged in with {provider.capitalize()}.', 'success')
    else:
        # New provider account
        if is_linking:
            # Link to current user
            create_auth_provider(provider, provider_user_info, token, current_user)
            flash(f'Your {provider.capitalize()} account has been linked.', 'success')
            return redirect(url_for('auth.link'))
        
        # Try to find a user with the same email
        if 'email' in provider_user_info and provider_user_info['email']:
            user = User.query.filter_by(email=provider_user_info['email']).first()
            if user:
                # User found, link provider to this user
                create_auth_provider(provider, provider_user_info, token, user)
                login_user(user)
                flash(f'Logged in with {provider.capitalize()} and linked to your existing account.', 'success')
            else:
                # Create new user and provider
                user = create_user_from_provider(provider_user_info)
                create_auth_provider(provider, provider_user_info, token, user)
                login_user(user)
                flash(f'Account created with {provider.capitalize()}.', 'success')
        else:
            # No email available, create new user
            user = create_user_from_provider(provider_user_info)
            create_auth_provider(provider, provider_user_info, token, user)
            login_user(user)
            flash(f'Account created with {provider.capitalize()}.', 'success')
    
    # Redirect to the next URL if it exists
    next_url = session.pop('next_url', None)
    return redirect(next_url or url_for('main.index'))

def create_user_from_provider(provider_user_info):
    """Create a new user from provider info."""
    user = User(
        username=provider_user_info.get('login') or provider_user_info.get('name'),
        email=provider_user_info.get('email'),
        display_name=provider_user_info.get('name'),
        picture_url=provider_user_info.get('avatar_url') or provider_user_info.get('picture')
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_auth_provider(provider, provider_user_info, token, user):
    """Create a new auth provider record."""
    auth_provider = AuthProvider(
        provider=provider,
        provider_user_id=provider_user_info['id'],
        access_token=token.get('access_token'),
        refresh_token=token.get('refresh_token'),
        token_expires_at=token.get('expires_at'),
        provider_username=provider_user_info.get('login') or provider_user_info.get('name'),
        provider_email=provider_user_info.get('email'),
        provider_picture=provider_user_info.get('avatar_url') or provider_user_info.get('picture'),
        user=user
    )
    db.session.add(auth_provider)
    db.session.commit()
    return auth_provider

def get_provider_user_info(provider, token):
    """Get user info from the provider API."""
    client = oauth.create_client(provider)
    
    if provider == 'github':
        resp = client.get('user')
        if resp.ok:
            user_info = resp.json()
            # Get email if not public
            if not user_info.get('email'):
                email_resp = client.get('user/emails')
                if email_resp.ok:
                    emails = email_resp.json()
                    primary_email = next((email for email in emails if email.get('primary')), None)
                    if primary_email:
                        user_info['email'] = primary_email.get('email')
            return user_info
    
    elif provider == 'google':
        resp = client.get('userinfo')
        if resp.ok:
            return resp.json()
    
    elif provider == 'discord':
        resp = client.get('users/@me')
        if resp.ok:
            return resp.json()
    
    elif provider == 'slack':
        resp = client.get('users.identity')
        if resp.ok:
            data = resp.json()
            if 'user' in data:
                return data['user']
    
    return None