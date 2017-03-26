# CollectionsModel.py
import sys
import logging
from datetime import datetime 
from MainModel import MainModel
from flask import flash
from AvispaLogging import AvispaLoggerAdapter
from couchdb.http import ResourceNotFound

class CollectionsModel:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
        
        self.MAM = MainModel(tid=tid,ip=ip)

    #COLLECTIONSMODEL
    def get_a_x(self,handle):

        # Returns list of collections

        try:               
            doc = self.MAM.select_user(handle) 
            collections = doc['collections']  
            rings = doc['rings'] 

            # 1. Here we need to call the DB again but now to get which 
            
            validring = {}
            ringorigins = {}
            ringcounts = {}


            for ring in rings:   

                if not 'deleted' in ring:
                    ringname = str(ring['ringname'])

                    if 'origin' in ring:
                        ringorigin = str(ring['origin'])
                    else:
                        ringorigin = str(handle)

                    ringorigins[ringname] = ringorigin 
                    ringcounts[ringname] = ring['count']

            #raise Exception('debug')
            self.lggr.info(ringcounts)
          
            for coll in collections:
                for ring in coll['rings']: 
                    if ring['ringname'] in ringcounts:   
                        ring['count'] = ringcounts[ring['ringname']]
                    if ring['ringname'] in ringorigins:
                        ring['ringorigin'] = ringorigins[ring['ringname']]
                                
            return collections
                

        except (ResourceNotFound, TypeError) as e:
            self.lggr.error("Notice: Expected error:%s,%s"%(sys.exc_info()[0] , sys.exc_info()[1]))
            

        return False

    
        

    #COLLECTIONSMODEL
    def post_a_x(self,handle,collectiond):
        '''Creates new collection'''

        doc = self.MAM.select_user(handle) 
        if 'description' not in collectiond:
            collectiond['description'] = ''

        newcollection = {'collectionname' : str(collectiond['name']),
                         'collectiondescription' : str(collectiond['description']),
                         'version' : str(collectiond['version']),
                         'rings' : collectiond['ringlist'],
                         'added' : str(datetime.now())}

        doc['collections'].append(newcollection)        
        self.MAM.post_user_doc(doc)
        return True  


    #COLLECTIONSMODEL
    def get_a_x_y(self,handle,collection):
        #Not used directly, but used by put_rq_a_x_y to return collection details
        #Returns just one collection

        try:               
            doc = self.MAM.select_user(handle) 

            

            collections = doc['collections'] 
            rings = doc['rings']
            
            validring = {}

            for ring in rings:   
                if not 'deleted' in ring:
                    ringname = str(ring['ringname'])
                    ringversion = str(ring['version'])
                    ringversionh = ringversion.replace('-','.')
                    validring[ringname+'_'+ringversionh] = ring['count']

            for coll in collections:
                #coll['valid'] = True
                if coll['collectionname'] == collection:
                    
                    #coll['valid'] = True
                    for ring in coll['rings']:       
                        if ring['ringname']+'_'+ring['version'] in validring:
                            ring['count'] = validring[ring['ringname']+'_'+ring['version']]
                        else:
                            pass
                            #InValid Collection, at least one of its rings is marked as deleted             
                            #coll['valid'] = False                             
                                
                    return coll

            return False
                    
                
        except (ResourceNotFound, TypeError) as e:
            self.lggr.error("Notice: Expected error:%s,%s"%(sys.exc_info()[0],sys.exc_info()[1]))
            

    #COLLECTIONSMODEL
    def put_a_x_y(self,handle,collectiond):

        doc = self.MAM.select_user(handle) 

        newcollection = {'collectionname' : str(collectiond['name']),
                         'collectiondescription' : str(collectiond['description']),
                         'version' : str(collectiond['version']),
                         'rings' : collectiond['ringlist'],
                         'added' : str(datetime.now())}

        i = 0
        for coll in doc['collections']:

            if coll['collectionname'] ==  newcollection['collectionname']:
                #This is a match. This is what we need to replace with incoming document
                doc['collections'][i] = newcollection

            i = i+1

        self.MAM.post_user_doc(doc)
        return True  


        #COLLECTIONSMODEL
    def patch_a_x_y(self,handle,collection,collectiond):

        doc = self.MAM.select_user(handle) 
        
        path = {}
        if 'name' in collectiond:
            patch['collectionname'] = str(collectiond['name'])
        if 'description' in collectiond:
            patch['collectiondescription'] = str(collectiond['description'])
        if 'version' in collectiond:
            patch['version'] = str(collectiond['version'])
        if 'rings' in collectiond:
            patch['rings'] = collectiond['ringlist']

        i = 0
        for coll in doc['collections']:

            if coll['collectionname'] ==  collection:
                
                for p in patch:
                    doc['collections'][i][p] = patch[p]

            i = i+1

        self.MAM.post_user_doc(doc)
        return True  

    def add_ring_to_collection(self,handle,collection,ringd):
 
        doc = self.MAM.select_user(handle) 
        for coll in doc['collections']:
            if coll['collectionname'] ==  collection:
                coll['rings'].append(ringd)

        self.lggr.info('Ring added to collection:',doc)
        self.MAM.post_user_doc(doc)
        return True

    #COLLECTIONSMODEL
    def delete_a_x_y(self,handle,collection):

        doc = self.MAM.select_user(handle) 

        i = 0
        for coll in doc['collections']:
            if coll['collectionname'] ==  collection:
                del doc['collections'][i] 

            i = i+1

        self.MAM.post_user_doc(doc)
        return True  
  