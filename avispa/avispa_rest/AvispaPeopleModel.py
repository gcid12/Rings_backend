# AvispaPeopleModel.py
import logging
import sys

from datetime import datetime 
from couchdb.http import ResourceNotFound
from flask import flash


import couchdb
from MainModel import MainModel
from env_config import COUCHDB_SERVER, COUCHDB_USER, COUCHDB_PASS
from flask.ext.login import current_user
from AvispaLogging import AvispaLoggerAdapter

class AvispaPeopleModel:

    def __init__(self,tid=None,ip=None):

        self.couch = couchdb.Server(COUCHDB_SERVER)
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.MAM = MainModel(tid=tid,ip=ip)

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})

    #PEOPLEMODEL
    def get_a_p(self,handle,person):
        pass

        # Returns list of people
        #Not being used. Using self.MAM.is_org(handle) instead. #FUTURE: Maybe we will have to use this in the future to optimize

    #PEOPLEMODEL
    def post_a_p(self,handle,person):
        '''Creates new person in the organization'''
                      
        doc = self.MAM.select_user(handle) 

        self.lggr.debug('user_doc[people]:%s'%doc['people'])

        newperson = {'handle': person,
                     'addedby': current_user.id,
                     'added': str(datetime.now())}

        doc['people'].append(newperson)

        return self.MAM.post_user_doc(doc)
 

    #PEOPLEMODEL
    def delete_a_p_q(self,handle,person):
        '''Deletes person from organization'''
        
        doc = self.MAM.select_user(handle)

        counter = 0
        for p in doc['people']:
            if p['handle'] == person:
                del doc['people'][counter]
            counter += 1

        return self.MAM.post_user_doc(doc)

  