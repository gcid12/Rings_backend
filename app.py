# Import flask and template operators
from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.bcrypt import Bcrypt
#
import os

# Define the WSGI application object
app = Flask(__name__)


# Configurations
app.config.from_object('default_config')

if app.config['DEBUG']:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)


# Flask BCrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)
# Associate Flask-Login manager with current app
login_manager = LoginManager()
login_manager.init_app(app)

oid = OpenID(app, os.path.join(app.config['BASE_DIR'], 'tmp'))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


