# Import flask and template operators
from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.bcrypt import Bcrypt
#
import os
import logging
from AvispaLogging import AvispaLoggerAdapter, LoggingSetUp

#import os
import json
import logging.config

# Define the WSGI application object
app = Flask(__name__)
# Configurations
app.config.from_object('default_config')


if 'DEBUG' in app.config:
    app_debug = app.config['DEBUG']
else:
    app_debug = True

#setup_logging()
LS = LoggingSetUp()
LS.setup(logfile_path=app.config['LOGFILE_PATH'],app_debug=app_debug)

logger = logging.getLogger('Avispa')
lggr = AvispaLoggerAdapter(logger, {'tid': '0','ip':'0'})


# Log something
lggr.info('Flask App defined!')
lggr.debug('Debug log is ON')


if app.config['DEBUG']:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)


# Flask BCrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)
# Associate Flask-Login manager with current app
login_manager = LoginManager()
lggr.info('Login Manager defined!')
login_manager.init_app(app)
lggr.info('Login Manager initialized!')
lggr.info(login_manager)

oid = OpenID(app, os.path.join(app.config['BASE_DIR'], 'tmp'))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


