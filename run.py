# Run a test server.
from avispa import avispa

if __name__ == "__main__":
	#avispa.run(host='0.0.0.0', port=80)
    avispa.run(host='127.0.0.1', port=8080, debug=True)
    
