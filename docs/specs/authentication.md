# Flaskapp Authentication

The Flaskapp authentication can use these auth providers:

- Github
- Google
- Discord
- Slack 

The code will use the providers that are configured depending on 
which of the the ``{name}_CLIENT_ID`` values are provided in the configuration. 

The .env file will hold the env vars. for instance: 


```bash
# http://localhost:5000/login/github/authorized
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# http://localhost:5000/login/google/authorized
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

The base configuration has a list of the provider names, ( [`github`, `google`,
`discord`, `slack`] ), and searches through them to find the client ID and
secret for each provider, registering the ones that are found. 



## Multiple Authentication Methods

The application supports multiple authentication methods per user, with the common
key either being the email address, for users that have previously logged in with 
another provider, or the user can explictly link multiple accounts
to the same user account. 


## UI

When a user tries to access a protected route, he will be redirected to the
application login screen, ( '/auth/login/' ) which provides buttons to login in
with any configured provider. The system will store the original URL the user
tried to access, and after successful authentication, the user will be
redirected back to that URL.

To support multiple accounts, there is a "Link Account" ( '/auth/link' )screen
that lists all of the available authentication providers. If the user is already
connected with one of the provider, the screen will show info for that account,
and a button to destroy the connection. 

For providers that the user is not connected to, the screen will show a button
to link the account. If the user clicks on the button, he will be redirected to
the provider's authentication page, and after successful authentication, the
user will be redirected back to the application, where the account will be
linked to the user account.


## User Model

The user model is defined in the `flaskapp/auth/models.py` file. It includes
fields that are common for user authentication and extra fields that
are specific to the auth providers. The database shall allow a user to 
have multiple authentication methods, so the user model is designed to
support multiple authentication methods per user.

# Routes

The authentication routes are defined in the `flaskapp/auth/routes.py` file.

The main route for authentication is `/auth/login/`, which  shows the user 
the login screen with buttons to login with the configured providers.
The `/auth/link/` route allows users to link additional accounts to their user profile.
The `/auth/logout/` route allows users to log out of the application.


## Implementation details 

All of the auth code is in a 'auth' blueprint, registered at '/auth/'

All of the authentication code for this
application is in the `flaskapp/auth` package. User logins is managed with 
`flask_login`.

It uses the `flask-dance` module, using the `make_<provider>_blueprint` functions
to create blueprints for each provider. The blueprints are registers with the 
prefix `/auth/<provider>/` where `<provider>` is the name of the provider

Auth specific templates are in the `flaskapp/auth/templates/auth` directory