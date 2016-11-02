#CollectionBuilder.py
import logging
from flask import flash
from CollectionsModel import CollectionsModel
from AvispaLogging import AvispaLoggerAdapter

class CollectionBuilder:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

        self.collectionprotocols = {}
        self.collectionprotocols['collectionprotocol'] = ['CollectioNname','CollectionDescription','CollectionVersion']
        self.collectionprotocols['mandatory'] = ['CollectionName']
        self.collectionprotocols['defaults'] = {'CollectionVersion':'0.1.0'}
        self.COM = CollectionsModel()
   
    def post_a_x(self,rqform,handle):
               
        if 'CollectionName' in rqform:
            collectiond = {}
            collectiond['name'] = rqform.get('CollectionName').lower() # I dont like this here
            collectiond['handle'] = handle.lower()

            if 'CollectionDescription' in rqform:
                collectiond['description'] = rqform.get('CollectionDescription').lower()
            else:
                collectiond['description'] = ''     
            if rqform.get('CollectionVersion'):
                collectiond['version'] = rqform.get('CollectionVersion').replace('.','-') # I dont like this here
            else:
                collectiond['version'] = self.collectionprotocols['defaults']['CollectionVersion'].replace('.','-')
            
            ringlist = []
          
            for p in rqform:
                pparts = p.split('_')
                ring = {}
                if pparts[0] == 'ring' and pparts[1]:
                    value = rqform.get(p)
                    vparts = value.split('_')
                    ring['handle'] = vparts[0]
                    ring['ringname'] = '_'.join(vparts[1:-1])
                    ring['version'] = vparts[-1].replace('.','-')
                    # Will implement this later. Layer is to separate from primary and secondary rings
                    ring['layer'] = 1 
                    ringlist.append(ring)

            collectiond['ringlist'] = ringlist
               
            #Here you write to the user.collection document
                     
            if self.COM.post_a_x(handle,collectiond):
                self.lggr.debug('New Collection created: '+collectiond['name'])
                return True
            else:
                self.lggr.debug('The Collection '+ collectiond['name'] +' database already exists')
                return False

    def put_a_x_y(self,rqform,handle,collection):

        #Same as collectiongenerator
        if rqform.get('CollectionName'):

            collectiond = {}

            collectiond['name'] = rqform.get('CollectionName').lower() # I dont like this here
            collectiond['description'] = rqform.get('CollectionDescription').lower()
            collectiond['handle'] = handle.lower()
            if rqform.get('CollectionVersion'):
                collectiond['version'] = rqform.get('CollectionVersion').replace('.','-') # I dont like this here
            
            
            ringlist = []
          
            for p in rqform:
                pparts = p.split('_')
                ring = {}
                if pparts[0] == 'ring' and pparts[1]:
                    value = rqform.get(p)
                    vparts = value.split('_')
                    ring['handle'] = vparts[0]
                    ring['ringname'] = vparts[1]
                    ring['version'] = vparts[2].replace('.','-')
                    # Will implement layer later. This is to separate from primary and secondary rings
                    ring['layer'] = 1 
                    ringlist.append(ring)

            collectiond['ringlist'] = ringlist
               
            #Here you write to the user.collection document
                     
            if self.COM.put_a_x_y(handle,collectiond):
                self.lggr.debug('Collection updated: '+collectiond['name'])
                return True
            else:
                self.lggr.debug('The Collection '+ collectiond['name'] +' database already exists')
                return False

