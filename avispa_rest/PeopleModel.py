# PeopleModel.py
import logging
import sys
from datetime import datetime 
from couchdb.http import ResourceNotFound
from flask import flash
from MainModel import MainModel
from flask.ext.login import current_user
from AvispaLogging import AvispaLoggerAdapter

class PeopleModel:

    def __init__(self,tid=None,ip=None):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
        
        self.MAM = MainModel(tid=tid,ip=ip)

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

        #Delete user from _people pool
        m = 0
        for people in doc['people']:
            if people['handle'] == person:
                del doc['people'][m]                
            m += 1

        #Delete user from all the teams it belongs too in this org (if any)
        n = 0  
        for team in doc['teams']: 
            p = 0 
            for m in team['members']:               
                if m['handle'] == person: 
                    del doc['teams'][n]['members'][p]
                p += 1
            n += 1

        return self.MAM.post_user_doc(doc)

  