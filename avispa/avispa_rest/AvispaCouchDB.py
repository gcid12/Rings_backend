# AvispaCouchDB.py
import couchdb
import os


class AvispaCouchDB:

    def _instantiate_couchdb_as_admin(self):

        couch = couchdb.Server()
        couch.resource.credentials = (os.environ['MYRING_COUCH_DB_USER'], 
        	                          os.environ['MYRING_COUCH_DB_PASS'])

        return couch 