# Flask Authentication

This module provides authentication functionality for the Flask application using OAuth providers:

- GitHub
- Google
- Discord
- Slack

## Configuration

Authentication is configured through environment variables. You can set these in a `.env` file:

```bash
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Discord OAuth
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret

# Slack OAuth
SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret
```

Only providers with both client ID and client secret configured will be enabled.

## Features

- Multiple authentication methods per user
- Account linking with multiple providers
- Profile management
- Secure session handling

## Usage

The authentication module provides the following routes:

- `/auth/login/` - Login page with buttons for all configured providers
- `/auth/logout/` - Logout functionality
- `/auth/link/` - Page to link/unlink authentication providers
- `/auth/profile/` - User profile management
- `/auth/<provider>/login` - Redirect to provider OAuth flow
- `/auth/<provider>/authorized` - OAuth callback URL

## Protected Routes

To protect a route, use the `@login_required` decorator:

```python
from flask_login import login_required

@app.route('/protected')
@login_required
def protected():
    return 'This page is protected'
```

## User Model

The User model provides the following fields:

- `id` - Primary key
- `username` - User's username
- `email` - User's email address
- `display_name` - User's display name
- `picture_url` - URL to the user's profile picture
- `auth_providers` - Relationship to authentication providers

Each authentication provider is stored in the `AuthProvider` model, which includes:

- Provider-specific identifiers
- Access and refresh tokens
- Profile information from the provider
