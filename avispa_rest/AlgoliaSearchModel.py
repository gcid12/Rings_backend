#ALGOLIA
from env_config import ALGOLIA_APPLICATION_ID,ALGOLIA_ADMIN_API_KEY
import algoliasearch

#LOGGING
import logging
import requests
from AvispaLogging import AvispaLoggerAdapter


class AlgoliaSearchModel:

    def __init__(self,handle,ring,tid=None,ip=None):
        
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

        client = algoliasearch.Client(ALGOLIA_APPLICATION_ID, ALGOLIA_ADMIN_API_KEY)
        indexname = '%-%'%(handle,ring)
        self.index = client.init_index(indexname)


    def post_item(self,content):

        r = self.index.add_object(content) 
        return check_status(r.status_code)

        
    def put_item(self,content,idx):

        object_id = '<idx>'
        r = self.index.add_object(content, object_id=idx)
        return check_status(r.status_code)
        

    def delete_item(self,idx):

        r = self.index.delete_object(self, idx)
        return check_status(r.status_code)

    def check_status(self,status)

        if r.status_code[0]=='2': 
            return True
        else:
            return False
        


