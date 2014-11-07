# Import flask and template operators
from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID


import os

# Define the WSGI application object
#avispa = Flask(__name__)
avispa = Flask(__name__)


# Configurations
avispa.config.from_object('default_config')
#avispa.config.from_object('env_config')
print('xx2')
print(os.path.join(avispa.config['BASE_DIR'], 'tmp'))

#
lm = LoginManager()
lm.init_app(avispa)
oid = OpenID(avispa, os.path.join(avispa.config['BASE_DIR'], 'tmp'))

# Sample HTTP error handling
@avispa.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


