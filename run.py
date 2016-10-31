import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Run a test server.
from app import app

# Import a module / component using its blueprint handler variable (mod_auth)
from avispa_rest.routes import avispa_rest
import TemplateFilters
from auth.auth import avispa_auth
from sandbox.sandbox import sandbox
from static_dev_server import static_dev_server
from flask import Blueprint

# Register blueprints

#Web server will intercept anything going to /static before it hits app
#This is used for dev envs
app.register_blueprint(static_dev_server)

#Production blueprints
app.register_blueprint(avispa_rest)
app.register_blueprint(avispa_auth)
app.register_blueprint(sandbox)


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=8000,threaded=True)
    
  
