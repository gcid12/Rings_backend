# MyRingCouchDB.py
import couchdb
import os


class MyRingCouchDB:

    def __init__(self):

        couch = couchdb.Server()
        self.couch = couch

    def instantiate_couchdb_as_admin(self):  
        #This is needed to have couch.resources available
        #for when couch.resources.credentials is created
        #Tried loading couch.resources.credentials here but it will only
        #load in the first instance. The following ones show None even though 
        #I call this function as well


        return self.couch 

    def _instantiate_couchdb_as_user(self,username=None,password=None):
        #WILL BE DEPRECATED

        if username and password:
            pass
            #self.couch.resource.credentials = (username,password)

        couch = couchdb.Server()

        return self.couch 
