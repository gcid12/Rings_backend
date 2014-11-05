# AvispaCouchDB.py
import couchdb
import os


class AvispaCouchDB:

    def __init__(self):

        self.couch = couchdb.Server()

    def _instantiate_couchdb_as_admin(self):

        
        # couch.resource.credentials = (os.environ['MYRING_COUCH_DB_USER'], 
        #                             os.environ['MYRING_COUCH_DB_PASS'])
        self.couch.resource.credentials = (u'admin',u'happy123')
        #print couch.resource.credentials
        return self.couch 

    def _instantiate_couchdb_as_user(self,username=None,password=None):

        if username and password:
            self.couch.resource.credentials = (username,password)

        couch = couchdb.Server()

        return self.couch 
