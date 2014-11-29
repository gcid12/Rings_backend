# Run a test server.
from app import app

# Import a module / component using its blueprint handler variable (mod_auth)
from avispa.avispa_rest.controllers import avispa_rest
from auth.auth import auth_flask_login
# Register blueprint(s)
app.register_blueprint(avispa_rest)
app.register_blueprint(auth_flask_login)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    #app.run(host='127.0.0.1', port=8080, debug=True)
    
