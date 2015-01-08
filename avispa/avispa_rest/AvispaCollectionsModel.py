# CollectionsModel.py

from datetime import datetime 
from couchdb.http import ResourceNotFound

from MyRingCouchDB import MyRingCouchDB
from MainModel import MainModel
from env_config import COUCHDB_USER, COUCHDB_PASS

class AvispaCollectionsModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD.instantiate_couchdb_as_admin()
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.user_database = 'myring_users'

        self.MAM = MainModel()


    #COLLECTIONSMODEL
    def get_a_x(self,handle,user_database=None):

        # Returns list of collections


        if not user_database : 
            user_database = self.user_database

        try:               
            db = self.MAM.select_db(user_database)
            user_doc = self.MAM.select_user(user_database,handle) 


            print('user_doc:',user_doc)

            collections = user_doc['collections']  
            rings = user_doc['rings']
            
            validring = {}

            for ring in rings:   
                if not 'deleted' in ring:
                    ringname = str(ring['ringname'])
                    ringversion = str(ring['version'])
                    ringversionh = ringversion.replace('-','.')
                    count = ring['count']
                    validring[ringname+'_'+ringversionh] = count

        

            for coll in collections:
                coll['valid'] = True
                for ring in coll['rings']:
                    
                    if ring['ringname']+'_'+ring['version'] not in validring:
                        #InValid Collection, at least one of its rings is marked as deleted             
                        coll['valid'] = False
                        break
                    else:
                        ring['count'] = validring[ring['ringname']+'_'+ring['version']]
                    
                        

            print('NewCollections:', collections)
                

        except (ResourceNotFound, TypeError) as e:
            print "Notice: Expected error:", sys.exc_info()[0] , sys.exc_info()[1]
            

        return collections

    
        

    #COLLECTIONSMODEL
    def post_a_x(self,handle,collection,user_database=None):

        #Creates new collection

        if not user_database : 
            user_database = self.user_database

                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        print('user_doc[colections]:',user_doc['collections'])

        newcollection = {'collectionname' : str(collection['name']),
                         'collectiondescription' : str(collection['description']),
                         'version' : str(collection['version']),
                         'rings' : collection['ringlist'],
                         'added' : str(datetime.now())}


        user_doc['collections'].append(newcollection)
        user_doc.store(db)

        return True  


    #COLLECTIONSMODEL
    def get_a_x_y(self,handle,collection,user_database=None):

        #Returns just one collection


        if not user_database : 
            user_database = self.user_database

        try:               
            db = self.MAM.select_db(user_database)
            user_doc = self.MAM.select_user(user_database,handle) 


            print('user_doc:',user_doc)

            collections = user_doc['collections'] 
            rings = user_doc['rings']
            
            validring = {}

            for ring in rings:   
                if not 'deleted' in ring:
                    ringname = str(ring['ringname'])
                    ringversion = str(ring['version'])
                    ringversionh = ringversion.replace('-','.')
                    count = ring['count']
                    validring[ringname+'_'+ringversionh] = count

            
            

            for coll in collections:
                #coll['valid'] = True
                if coll['collectionname'] == collection:
                    
                    for ring in coll['rings']:       
                        if ring['ringname']+'_'+ring['version'] not in validring:
                            #InValid Collection, at least one of its rings is marked as deleted             
                            coll['valid'] = False
                            break
                        else:
                            ring['count'] = validring[ring['ringname']+'_'+ring['version']]
                                            
                    return coll
                        

            #print('ValidatedCollections:', collections)
                

        except (ResourceNotFound, TypeError) as e:
            print "Notice: Expected error:", sys.exc_info()[0] , sys.exc_info()[1]
            


    #COLLECTIONSMODEL
    def put_a_x_y(self,handle,collectiond,user_database=None):

        if not user_database : 
            user_database = self.user_database

                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        print('user_doc[colections]:',user_doc['collections'])

        newcollection = {'collectionname' : str(collectiond['name']),
                         'collectiondescription' : str(collectiond['description']),
                         'version' : str(collectiond['version']),
                         'rings' : collectiond['ringlist'],
                         'added' : str(datetime.now())}

        i = 0
        for coll in user_doc['collections']:

            #print()
            #print('coll',coll)
            #print('user_doc[collections][i]',user_doc['collections'][i])
            #print()
            #print('coll[collectioname]:',coll['collectionname'])
            #print('newcoll:',newcollection['collectionname'])
            if coll['collectionname'] ==  newcollection['collectionname']:
                print ('You need to replace this', coll)
                print ('For this:', newcollection)
                #This is a match. This is what we need to replace with incoming document
                user_doc['collections'][i] = newcollection
                #print ('coll MOD',coll)


            i = i+1

                #user_doc['collections'].append(newcollection)
        print('user_doc MOD:',user_doc)
        user_doc.store(db)

        return True  


    #COLLECTIONSMODEL
    def delete_a_x_y(self,handle,collection,user_database=None):

        if not user_database : 
            user_database = self.user_database

                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        i = 0
        for coll in user_doc['collections']:
            if coll['collectionname'] ==  collection:
                del user_doc['collections'][i] 

            i = i+1

        print('user_doc MOD:',user_doc)
        user_doc.store(db)

        return True  
  