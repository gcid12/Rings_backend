# MyRingTool.py

import uuid
import random
import bcrypt
import json


from flask import flash

from MainModel import MainModel
from AvispaModel import AvispaModel

from auth.AuthModel import AuthModel

from AvispaUpload import AvispaUpload
from CouchViewSync import CouchViewSync
from MyRingSchema import MyRingSchema
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)



class MyRingPatch:

    def __init__(self):

        self.AVM = AvispaModel() 
        self.MAM = MainModel() 
        self.ATM = AuthModel()  
        self.user_database = 'myring_users'  

  

    def p20141208(self,request,*args):

        from MyRingCouchDB import MyRingCouchDB
        from MyRingUser import MyRingUser
        from env_config import COUCHDB_USER, COUCHDB_PASS
        from couchdb.design import ViewDefinition


        MCD = MyRingCouchDB()
        self.couch=MCD.instantiate_couchdb_as_admin()    
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)

        print('patch_20141208')

        print(current_user.username)

        
        #db = self.couch[self.user_database]
        #user =  MyRingUser.load(db,current_user)

        user = self.MAM.select_user(self.user_database,current_user.username)

        if user:

            for ring in user['rings']:

                db_ringname=current_user.username+'_'+str(ring['ringname'])+'_'+str(ring['version'])
                print(db_ringname)
                db2 = self.couch[db_ringname]
                if not MyRingSchema.load(db2,'schema'):
                    schema = MyRingSchema.load(db2,'blueprint')
                    print('Schema:',schema)
                    schema._id= 'schema' 
                    schema.store(db2)
                
                view = ViewDefinition('ring', 'schema', 
                       '''
                        function(doc) {
                          if(doc._id=='schema'){   
                            emit(doc._id, doc)
                          }
                        }
                       ''')

                view.get_doc(db2)
                view.sync(db2)



        d = {'rq': current_user,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d





            





















