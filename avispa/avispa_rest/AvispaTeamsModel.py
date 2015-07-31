# AvispaTeamsModel.py
import sys

from datetime import datetime 
from couchdb.http import ResourceNotFound

import couchdb
from MainModel import MainModel
from env_config import COUCHDB_SERVER,COUCHDB_USER, COUCHDB_PASS
from flask.ext.login import current_user 
from flask import flash, current_app

class AvispaTeamsModel:

    def __init__(self):

        self.couch = couchdb.Server(COUCHDB_SERVER)
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        self.user_database = 'myring_users'
        self.MAM = MainModel()

    #TEAMSMODEL
    def post_a_m_n_members(self,handle,team,member,user_database=None):
        #Creates new member in the team

        if not user_database : 
            user_database = self.user_database
                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        current_app.logger.debug(user_doc['teams'])


        for teamd in user_doc['teams']:
            if teamd['teamname'] == team:
                current_app.logger.debug('Members for team '+team,teamd['members'])
                memberlist = []

                if 'members' not in teamd:
                    teamd['members'] = []


                for memberd in teamd['members']:
                    memberlist.append(memberd['handle'])

                if member in memberlist:
                    #User is already memberm abort adding a member                  
                    return False                      
                else:
                    newmember = {'handle': member,
                     'addedby': current_user.id,
                     'added': str(datetime.now())}
                    teamd['members'].append(newmember)
                    
                break

        user_doc.store(db)
        return True 


    #TEAMSMODEL
    def delete_a_m_n_members(self,handle,team,member,user_database=None):
        #Deletes an existing member from the team

        if not user_database : 
            user_database = self.user_database
                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        current_app.logger.debug(user_doc['teams'])

        count1 = 0
        for teamd in user_doc['teams']:
            if teamd['teamname'] == team:
                current_app.logger.debug('Members for team '+team,teamd['members'])
                memberlist = []
                count2 = 0
                for memberd in teamd['members']:
                    if member == memberd['handle']:
                        del user_doc['teams'][count1]['members'][count2]
                    count2 += 1
            count1 += 1
                    
        if user_doc.store(db):
            return True 
        else:
            return False


    #TEAMSMODEL
    def post_a_m_n_rings(self,handle,team,ring,user_database=None):
        #Creates new member in the team

        if not user_database : 
            user_database = self.user_database
                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        current_app.logger.debug(user_doc['teams'])


        for teamd in user_doc['teams']:
            if teamd['teamname'] == team: 
                ringlist = []

                if 'rings' not in teamd:
                    teamd['rings'] = []


                for ringd in teamd['rings']:
                    ringlist.append(ringd['ringname'])

                if ring in ringlist:
                    #Ring is already in the team list                
                    return False                      
                else:
                    newring = {'handle' : handle,
                     'ringname': ring,
                     'addedby': current_user.id,
                     'added': str(datetime.now())}
                    teamd['rings'].append(newring)
                    
                break

        user_doc.store(db)
        return True 



        #TEAMSMODEL
    def delete_a_m_n_rings(self,handle,team,ring,user_database=None):
        #Deletes an existing member from the team

        if not user_database : 
            user_database = self.user_database
                      
        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        current_app.logger.debug(user_doc['teams'])

        count1 = 0
        for teamd in user_doc['teams']:
            if teamd['teamname'] == team:
                ringlist = []
                count2 = 0
                for ringd in teamd['rings']:
                    if ring == ringd['ringname']:
                        del user_doc['teams'][count1]['rings'][count2]
                    count2 += 1
            count1 += 1
                    
        if user_doc.store(db):
            return True 
        else:
            return False
 
    def put_a_m_n_settings(self,handle,team,parameters,user_database=None):

        if not user_database : 
            user_database = self.user_database

        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        for teamd in user_doc['teams']:
            if teamd['teamname'] == team: 
                if 'description' in parameters:
                    teamd['description'] = parameters['description']

                if 'teamauth' in parameters: 

                    teamd['roles'] = []

                    if parameters['teamauth'] == 'RWX':
                        role = 'team_admin'

                    elif parameters['teamauth'] == 'RW':  
                        role = 'team_writer'
                 
                    elif parameters['teamauth'] == 'R':
                        role = 'team_reader'
                    else:
                        role = False
                        
                    if role:

                        newrole = {'handle' : handle,
                         'role': role,
                         'addedby': current_user.id,
                         'added': str(datetime.now())}
                        teamd['roles'].append(newrole)

                break;

        if user_doc.store(db):
            return True 
        else:
            return False

  