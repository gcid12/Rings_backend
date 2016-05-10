import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Run a test server.
from app import app

# Import a module / component using its blueprint handler variable (mod_auth)
from avispa.avispa_rest.controllers import avispa_rest
import TemplateFilters
from auth.auth import auth_flask_login
from sandbox.sandbox import sandbox
# Register blueprint(s)
app.register_blueprint(avispa_rest)
app.register_blueprint(auth_flask_login)
app.register_blueprint(sandbox)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=8000,threaded=True)
    
  
