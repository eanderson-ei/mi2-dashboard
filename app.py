import dash
import dash_bootstrap_components as dbc
import dash_auth
import json
import os

external_stylesheets = [dbc.themes.FLATLY]  # Also try LITERA, SPACELAB

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, show_undo_redo=True)
server = app.server
app.config.suppress_callback_exceptions = True

# Keep this out of source code repository - save in a file or a database
# Local dev
try:
    with open('secrets/passwords.json') as f:
        VALID_USERNAME_PASSWORD_PAIRS = json.load(f)
# Heroku dev
except:
    json_creds = os.environ.get("VALID_USERNAME_PASSWORD_PAIRS")
    VALID_USERNAME_PASSWORD_PAIRS = json.loads(json_creds)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)