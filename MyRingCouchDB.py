# MyRingCouchDB.py
import couchdb
import os
from env_config import COUCHDB_SERVER, COUCHDB_USER, COUCHDB_PASS


class MyRingCouchDB:

    def __init__(self):

        
        self.couch = couchdb.Server(COUCHDB_SERVER)
        

    def instantiate_couchdb_as_admin(self):


        #self.couch = couchdb.Server()

        
        # couch.resource.credentials = (os.environ['MYRING_COUCH_DB_USER'], 
        #                             os.environ['MYRING_COUCH_DB_PASS'])
        #self.couch.resource.credentials = (u'admin',u'happy123')
        #print couch.resource.credentials
        return self.couch 

    def instantiate_couchdb_as_user(self,username=None,password=None):


        #self.couch = couchdb.Server()
        #couch = couchdb.Server("https://%s.cloudant.com" % username)

        return self.couch 
