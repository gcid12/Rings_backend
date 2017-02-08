from env_config import ALGOLIA_APPLICATION_ID,ALGOLIA_ADMIN_API_KEY

#LOGGING
import logging
from AvispaLogging import AvispaLoggerAdapter


class AlgoliaSearchModel:

    def __init__(self,handle,ring,tid=None,ip=None):
        
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

        client = algoliasearch.Client(ALGOLIA_APPLICATION_ID, ALGOLIA_ADMIN_API_KEY)
        indexname = '%-%'%(handle,ring)
        self.index = client.init_index(indexname)
        


    def index_item(self,handle,ring,idx):

    	
        
    	

    def unindex_item(self,handle,ring,idx):
    	
    	
        

    def config_index:
    	
    	
        

    



