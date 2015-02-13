# AvispaTeamsModel.py
import sys

from datetime import datetime 
from couchdb.http import ResourceNotFound

from MyRingCouchDB import MyRingCouchDB
from MainModel import MainModel
from env_config import COUCHDB_USER, COUCHDB_PASS
from flask.ext.login import current_user

class AvispaTeamsModel:

    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD.instantiate_couchdb_as_admin()
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

        print(user_doc['teams'])


        for teamd in user_doc['teams']:
            if teamd['teamname'] == team:
                print('Members for team '+team,teamd['members'])
                memberlist = []
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

        print(user_doc['teams'])

        count1 = 0
        for teamd in user_doc['teams']:
            if teamd['teamname'] == team:
                print('Members for team '+team,teamd['members'])
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
 
  