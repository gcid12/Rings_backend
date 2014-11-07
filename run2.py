# Run a test server.
from app import app

# Import a module / component using its blueprint handler variable (mod_auth)
from avispa.avispa_rest.controllers import avispa_rest
# Register blueprint(s)
app.register_blueprint(avispa_rest)

if __name__ == "__main__":
	#avispa.run(host='0.0.0.0', port=80)
    app.run(host='127.0.0.1', port=8080, debug=True)
    
