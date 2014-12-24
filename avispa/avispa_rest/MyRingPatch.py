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

                db_ringname=current_user.username+'_'+str(ring['ringname'])
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



    def p20141223(self,request,*args):

        #Select schema for this Ring
        print('check_and_repair_ring')

        handle = request.args.get('handle')
        ringname = request.args.get('ringname')

        print('handle:',handle)
        print('ringname:',ringname)

        if handle and ringname:
            schema = self.AVM.ring_get_schema_from_view(handle,ringname)
            #print('schema:',schema['fields'])

            #Pre: Obtain the fields
            fieldlist = []
            for f in schema['fields']:
                fieldlist.append(f['FieldName'])

            print('fieldlist:',fieldlist)


            
            #Pre: Obtain the items
            items = self.AVM.get_a_b(handle,ringname,limit=1000000)
            itemlist = []
            for i in items:
                itemlist.append(i['_id'])
                
            print('itemlist:',itemlist)

            #Get each one of the items and check its structure


            
            for idx in itemlist:
               
                #item = self.AVM.get_a_b_c(None,handle,ringname,idx)

                #item_x = self.AVM.ring_get_item_document(handle,ringname,idx)

                from MyRingCouchDB import MyRingCouchDB
                from env_config import COUCHDB_USER, COUCHDB_PASS
                from datetime import datetime 

                db_ringname=str(handle)+'_'+str(ringname)

                MCD = MyRingCouchDB()
                self.couch=MCD.instantiate_couchdb_as_admin()    
                self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)

                db = self.couch[db_ringname]

                schema = self.AVM.ring_get_schema(handle,ringname)
                RingClass = self.AVM.ring_create_class(schema)
                item_x = RingClass.load(db,idx)

                #print('item_x:',item_x)
                print('item_x[items]:',item_x['items'])

                needs_saving=False
 
                
                #CHECK 1 : Complete Fields in items[]

                for f_x in fieldlist:
                    if 'items' in item_x:
                        if len(item_x['items'])>0:
                            if f_x in item_x['items'][0]:
                                print(f_x+' exists in items[]')
                            else: 
                                print(f_x+' does not exist in items[]')
                                #fix it
                                item_x['items'][0][f_x]=''
                                print('FIXED: '+f_x+' does not exist in items[]')
                                needs_saving=True
                        else:
                            print('Empty items[]')
                            #fix it
                            items_dictionary = {}
                            items_dictionary[f_x] = ''
                            item_x['items'].append(items_dictionary)
                            print('FIXED: Empty items[]')
                            needs_saving=True
                    else:
                        print('items[] does not even exist')
                        #fix it
                        item_x['items']=[]
                        items_dictionary = {}
                        items_dictionary[f_x] = ''
                        item_x['items'].append(items_dictionary)
                        print('FIXED: items[] does not even exist')
                        needs_saving=True

                #CHECK 2 : Complete Fields in rich[]

                for f_x in fieldlist:
                    if 'rich' in item_x:
                        if len(item_x['rich'])>0:
                            if f_x in item_x['rich'][0]:
                                print(f_x+' exists in rich[]')
                            else: 
                                print(f_x+' does not exist in rich[]')
                                #fix it
                                item_x['rich'][0][f_x]={}
                                print('FIXED: '+f_x+' does not exist in rich[]')
                                needs_saving=True
                        else:
                            print('Empty rich[]')
                            #fix it
                            rich_dictionary = {}
                            rich_dictionary[f_x] = {}
                            item_x['rich'].append(rich_dictionary)
                            print('FIXED: Empty rich[]')
                            needs_saving=True

                    else:
                        print('rich[] does not even exist')
                        #fix it
                        item_x['rich']=[]
                        rich_dictionary = {}
                        rich_dictionary[f_x] = {}
                        item_x['rich'].append(rich_dictionary)
                        print('FIXED: rich[] does not even exist')
                        needs_saving=True


                #CHECK 3 : Complete Fields in history[]

                for f_x in fieldlist:
                    if 'history' in item_x:
                        if len(item_x['history'])>0:
                            if f_x in item_x['history'][0]:
                                print(f_x+' exists in history[]')
                            else: 
                                print(f_x+' does not exist in history[]')
                                #fix it
                                item_x['history'][0][f_x]=[]
                                print('FIXED: '+f_x+' does not exist in history[]')
                                needs_saving=True
                        else:
                            print('Empty history[]')
                            #fix it
                            history_dictionary = {}
                            history_dictionary[f_x] = []
                            #history_item = {}
                            #history_item['date']= str(datetime.now())
                            #history_item['after']='HISTORY UPDATED'
                            #history_item['author']=handle
                            #history_item['before']=''
                            #history_dictionary[f_x].append(history_item)
                            item_x['history'].append(history_dictionary)
                            print('FIXED: Empty history[]')
                            needs_saving=True
                    else:
                        print('history[] does not even exist')
                        #fix it
                        item_x['history']=[]
                        history_dictionary = {}
                        history_dictionary[f_x] = []
                        #history_item = {}
                        #history_item['date']= str(datetime.now())
                        #history_item['after']='HISTORY UPDATED'
                        #history_item['author']=handle
                        #history_item['before']=''
                        #history_dictionary[f_x].append(history_item)
                        item_x['history'].append(history_dictionary)
                        print('FIXED: history[] does not even exist')
                        needs_saving=True


                if needs_saving:
                    if item_x.store(db): 
                        print('item document saved:',item_x)
                else:
                    print('Nothing to patch here')   

        else:
            print('Please indicate this in URL:  ?handle=x&ringname=y')  
                

        d = {'rq': current_user,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d








            





















