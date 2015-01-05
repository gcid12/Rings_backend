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


    #AVISPAMODEL
    def get_collections(self,handle,user_database=None):


        if not user_database : 
            user_database = self.user_database

        try:               
            db = self.MAM.select_db(user_database)
            user_doc = self.MAM.select_user(user_database,handle) 


            print('user_doc:',user_doc)

            collections = user_doc['collections']  
                

        except (ResourceNotFound, TypeError) as e:
            print "Notice: Expected error:", sys.exc_info()[0] , sys.exc_info()[1]
            

        return collections


    def set_collection(self,handle,collection,user_database=None):

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