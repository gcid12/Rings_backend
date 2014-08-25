# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
avispa = Flask(__name__)

# Configurations
avispa.config.from_object('config')


# Sample HTTP error handling
@avispa.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from avispa.avispa_web.controllers import avispa_web

# Register blueprint(s)
avispa.register_blueprint(avispa_web)
