import os
import json
import time
import logging.config
import logging



class LoggingSetUp:

    def setup(
        self,
        logfile_path=None,
        config_path='logging.json', 
        default_level=logging.INFO,
        env_key='LOG_CFG',
        app_debug = False
    ):
        """Setup logging configuration

        """
        path = config_path            
        print('path: '+str(path))        
        if path:
            dir = os.path.dirname(__file__)  
            path = os.path.join(dir,path)
            print('Retrieving log config file from '+path)
            if os.path.exists(path):
                print('The path exists')
                with open(path, 'rt') as f:
                    config = json.load(f)
                    if logfile_path:

                        for han in config['handlers']:
                            if config['handlers'][han]['class'] == 'logging.handlers.RotatingFileHandler':
                                filename = config['handlers'][han]['filename']
                                config['handlers'][han]['filename'] = logfile_path+'/'+filename
                                print("Logfile:"+config['handlers'][han]['filename'])

                            
                            print('app_debug',app_debug)
                            if app_debug != True:

                                #Don't let DEBUG run if app_debug is not  DEBUG
                                if config['handlers'][han]['level'] == 'DEBUG':
                                    config['handlers'][han]['level'] = 'INFO'


                    logging.config.dictConfig(config)

            else:
                print('The path does not exist')
                logging.basicConfig(level=default_level)
                           
        else:
            print('basic logging')
            logging.basicConfig(level=default_level)



class AvispaLoggerAdapter(logging.LoggerAdapter):
    """
    This adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '[%s-%s] +- %s' % (self.extra['ip'],self.extra['tid'], msg), kwargs

