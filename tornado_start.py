from AvispaLogging import AvispaLoggerAdapter
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from run import app
from env_config import NUMBER_OF_PROCESSES


def main():

	http_server = HTTPServer(WSGIContainer(app))


	# One Process
	#http_server.listen(5000)

	
	# Multi Process
	http_server.bind(8000)
	http_server.start(NUMBER_OF_PROCESSES) # forks one process per cpu
	

	IOLoop.instance().start()



if __name__ == '__main__':
    main()

