#ALGOLIA
from env_config import ALGOLIA_APPLICATION_ID,ALGOLIA_ADMIN_API_KEY
from algoliasearch import algoliasearch

#LOGGING
import logging
import requests
from AvispaLogging import AvispaLoggerAdapter


class AlgoliaSearchModel:

    def __init__(self,handle,ring,tid=None,ip=None):
        
        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

        self.handle = handle
        self.ring = ring

        client = algoliasearch.Client(ALGOLIA_APPLICATION_ID, ALGOLIA_ADMIN_API_KEY)
        indexname = '%s-%s'%(handle,ring)
        self.index = client.init_index(indexname)

        
    def indexer(self,content,idx):
        print content

        item = self.clean_content(content)

        self.lggr.info('Algolia Indexing %s/%s/%s'%(self.handle,self.ring,idx))
        self.lggr.info('Item to index: %s'%(item))

       
        r = self.index.add_object(item, object_id=idx)
        print(r)
        return r
        

    def unindexer(self,idx):

        r = self.index.delete_object(self, idx)
        return check_response_status(r.status_code)

    def clean_content(self,content):

        item = content['item']

        clean = {}

        for k in item:
            if k[0] != '_':
                if k[-5:] != '_flag':
                    if k[-5:] != '_rich':
                        clean[k] = item[k]

        return clean



        


