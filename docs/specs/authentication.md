# Flaskapp Authentication

The Flaskapp authentication can use these auth providers:

- Github
- Google
- Discord
- Slack 

The code will use the providers that are configured depending on 
which of the the ``{name}_CLIENT_ID`` values are provided in the configuration. 


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


## Implementation details 

It uses the `authlib` module. All of the authentication code for this
application is in the `flaskapp/auth` package. User logins is managed with 
`flask_login`.

Auth specific templates are in the `flaskapp/auth/templates/auth` directory