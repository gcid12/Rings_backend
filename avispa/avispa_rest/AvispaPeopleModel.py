# AvispaPeopleModel.py
import sys

from datetime import datetime 
from couchdb.http import ResourceNotFound
from flask import flash, current_app


import couchdb
from MainModel import MainModel
from env_config import COUCHDB_SERVER, COUCHDB_USER, COUCHDB_PASS
from flask.ext.login import current_user

class AvispaPeopleModel:

    def __init__(self):

        self.couch = couchdb.Server(COUCHDB_SERVER)
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.user_database = 'myring_users'

        self.MAM = MainModel()


    #PEOPLEMODEL
    def get_a_p(self,handle,person,user_database=None):
        pass

        # Returns list of people

        #Not being used. Using self.MAM.is_org(handle) instead. #FUTURE: Maybe we will have to use this in the future to optimize

    
        

    #PEOPLEMODEL
    def post_a_p(self,handle,person,user_database=None):

        #Creates new person in the organization

        if not user_database : 
            user_database = self.user_database

                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        current_app.logger.debug('user_doc[people]:',user_doc['people'])

        newperson = {'handle': person,
                     'addedby': current_user.id,
                     'added': str(datetime.now())}

        user_doc['people'].append(newperson)
        user_doc.store(db)

        return True  


    #PEOPLEMODEL
    def delete_a_p_q(self,handle,person,user_database=None):

        #Deletes person from organization

        if not user_database : 
            user_database = self.user_database

                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        current_app.logger.debug('user_doc[people]:',user_doc['people'])

        counter = 0
        for p in user_doc['people']:
            if p['handle'] == person:
                del user_doc['people'][counter]
            counter += 1


        user_doc.store(db)

        return True

 
  