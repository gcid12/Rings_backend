import logging

class AvispaLoggerAdapter(logging.LoggerAdapter):
    """
    This adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '[%s-%s] - %s' % (self.extra['ip'],self.extra['tid'], msg), kwargs


import os
import json
import time
import logging.config


class LoggingSetUp:

   	def setup(
   		self,
   		logfile_path=None,
	    default_path='logging.json', 
	    default_level=logging.INFO,
	    env_key='LOG_CFG'
	):
	    """Setup logging configuration

	    """
	    path = default_path
            
	    value = os.getenv(env_key, None)
	    if value:
	        path = value
            dir = os.path.dirname(__file__)  
            path = os.path.join(dir,path)
            if os.path.exists(path):
	        with open(path, 'rt') as f:
	            config = json.load(f)
	            if logfile_path:
	            	localtime = time.localtime()
	            	datestring = time.strftime("%Y%m%d",localtime)

                    for han in config['handlers']:
                    	if config['handlers'][han]['class'] == 'logging.handlers.RotatingFileHandler':
                            filename = config['handlers'][han]['filename']
                            config['handlers'][han]['filename'] = logfile_path+'/'+datestring+filename
                            print("Logfile:"+config['handlers'][han]['filename'])
    	
	        logging.config.dictConfig(config)
	    else:
                print('basic logging')
	        logging.basicConfig(level=default_level)
