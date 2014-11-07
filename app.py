# Import flask and template operators
from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID


import os

# Define the WSGI application object
#app = Flask(__name__)
app = Flask(__name__)


# Configurations
app.config.from_object('default_config')
#app.config.from_object('env_config')
#print(os.path.join(app.config['BASE_DIR'], 'tmp'))

#
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(app.config['BASE_DIR'], 'tmp'))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


