from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, login_required, current_user

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

    pre_auth_url = session.get('pre_auth_url')
    if pre_auth_url:
        # Clear the pre-auth URL after using it
        session.pop('pre_auth_url', None)
    
        
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


@auth_bp.route('/google/authorized')
def google_authorized():
    """Callback route after provider authorization."""
  
    print(f"Provider: google")


@auth_bp.route('/github/authorized')
def github_authorized():
    """Callback route after provider authorization."""
    from flask_dance.contrib.github import github

    if not github.authorized:
        flash('GitHub authorization failed.', 'danger')
        return redirect(url_for('auth.login'))

    # Get the response from GitHub API
    resp = github.get('user')
    if not resp.ok:
        flash('Failed to get user info from GitHub.', 'danger')
        return redirect(url_for('auth.login'))

    # Get user info
    user_info = resp.json()

    print(f"User info: {user_info}")

    # Print all session data for debugging
    print("GitHub session data:")
    for key, value in github.__dict__.items():
        print(f"{key}: {value}")

    # Alternative way to access the session data
    token = github.token
    print(f"Access token: {token}")


    if session.get('next_url'):
        next_url = session.pop('next_url')
    else:
        next_url = url_for('main.index')
    # Check if the user already exists
    user = User.query.filter_by(email=user_info.get('email')).first()
    if not user:
        # Create a new user if not found
        user = create_user_from_provider(user_info)
    else:
        # Update existing user info
        user.username = user_info.get('login') or user_info.get('name')
        user.email = user_info.get('email')
        user.display_name = user_info.get('name')
        user.picture_url = user_info.get('avatar_url') or user_info.get('picture')
        db.session.commit()
    # Create or update the auth provider record
    auth_provider = AuthProvider.query.filter_by(
        user_id=user.id, 
        provider='github', 
        provider_user_id=str(user_info['id'])  # Convert ID to string to match db column type
    ).first()
    if not auth_provider:
        auth_provider = create_auth_provider('github', user_info, token, user)
    else:
        auth_provider.access_token = token.get('access_token')
        auth_provider.refresh_token = token.get('refresh_token')
        auth_provider.token_expires_at = token.get('expires_at')
        auth_provider.provider_username = user_info.get('login') or user_info.get('name')
        auth_provider.provider_email = user_info.get('email')
        auth_provider.provider_picture = user_info.get('avatar_url') or user_info.get('picture')
        db.session.commit()
    # Log the user in
    login_user(user)
    flash('You have successfully logged in with GitHub.', 'success')
    return redirect(next_url)





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
        provider_user_id=str(provider_user_info['id']),  # Convert ID to string
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