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
        '''
        This patch pulls every single item and checks whether its document has the correct structure
        @input (GET): handle
        @input (GET): ringname

        '''

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





    def p20150105(self,request,*args):

        print('check_and_repair_user')

        handle = request.args.get('handle')
        
        print('handle:',handle)

        if not request.args.get('user_database'): 
            user_database = 'myring_users'

        db = self.MAM.select_db(user_database)
        user_doc = self.MAM.select_user(user_database,handle) 

        try:

            print('user_doc[colections]:',user_doc['collections'])

        except(KeyError):

            user_doc['collections'] = []        
            user_doc.store(db)

            print('User: '+handle+' repaired.')

        d = {'rq': current_user,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d

            
    def p20150113(self,request,*args):
        '''
        This patch repairs items that where affected by the bug that didn't detect rich fields. 
        It detects affected items and aquires rich-data from the source
        @input (GET) : handle
        @input (GET) : ringname
        '''

        print('Starts patch p20150113')


        from MyRingCouchDB import MyRingCouchDB
        from env_config import COUCHDB_USER, COUCHDB_PASS
        from datetime import datetime

        import urlparse
        import requests

        MCD = MyRingCouchDB()
        self.couch=MCD.instantiate_couchdb_as_admin()    
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
                
   

        handle = request.args.get('handle')
        ringname = request.args.get('ringname')

        print('handle:',handle)
        print('ringname:',ringname)

        if handle and ringname:
            schema = self.AVM.ring_get_schema_from_view(handle,ringname)
            #print('schema:',schema['fields'])

            
            #Pre: Obtain the items
            items = self.AVM.get_a_b(handle,ringname,limit=1000000)
            itemlist = []
            for i in items:
                itemlist.append(i['_id'])
                
            print('itemlist:',itemlist)


            #schema = self.AVM.ring_get_schema(handle,ringname)
            RingClass = self.AVM.ring_create_class(schema)
            db_ringname=str(handle)+'_'+str(ringname)
            db = self.couch[db_ringname]

            
            for idx in itemlist: 
                #For each item in the Ring            
    
                item = RingClass.load(db,idx)
                needs_saving = False

                for field in schema['fields']:
                    #For each field in the item
                    if field['FieldWidget'] == 'select' and field['FieldSource']:
                        #If it is a select 
                        if item.items[0][field['FieldName']]:
                            #If it exists

                            try: 
                                external_id = int(item['items'][0][field['FieldName']])
                            except:
                                break


                            if external_id:

                                needs_saving = True

                                #If it is an integer

                                #Retrieve it and see if it exists
                                urlparts = urlparse.urlparse(field['FieldSource'])
                                print('urlparts',urlparts)

                                pathparts = urlparts.path.split('/')
                                if pathparts[1]!='_api':
                                    corrected_path = '/_api'+urlparts.path
                                    external_handle = pathparts[1]
                                    external_ringname = pathparts[2]
                                else:
                                    corrected_path = urlparts.path
                                    external_handle = pathparts[2]
                                    external_ringname = pathparts[3]

                                path = corrected_path+'/'+str(external_id)
                                query = 'schema=1'
                                url=urlparse.urlunparse((urlparts.scheme, urlparts.netloc, path , '', query, ''))

                                external_host=urlparse.urlunparse((urlparts.scheme, urlparts.netloc, '', '', '', ''))
                                print('external_host:',external_host)

                                rqurl = urlparse.urlparse(request.url)
                                local_host=urlparse.urlunparse((rqurl.scheme, rqurl.netloc, '', '', '', ''))
                                print('local_host:',local_host)

                                if local_host==external_host:
                                    print('Data source is in the same server')

                                    rich_item = self.AVM.get_a_b_c(None,external_handle,external_ringname,external_id)

                                    rs = self.AVM.ring_get_schema_from_view(external_handle,external_ringname)

                                    print('rich_rs:',rs)
                                    print('rich_item:',rich_item)
                                    
                                    external_FieldName = rs['fields'][0]['FieldName']

                                    
                                else:
                                    print('Data source is in another server')
                                 
                                    print('Retrieving source at:',url)
                                    r = requests.get(url)
                                    print('Raw JSON schema:')
                                    print(r.text)
                                    rs = json.loads(r.text)
                                    print('rich_rs:',rs)
                                    rich_item = rs['items'][0]
                                    print('rich_item:',rich_item)
                                    external_FieldName = rs['fields'][0]['FieldName']

                                if not rich_item:
                                    #It didn't find the external item
                                    break


                                rich_item_dict = {}
                                #Nice to include where we got the information from
                                rich_item_dict['_source'] = url  
                                # Converting the ordered_dictionary to regular dictionary
                                for j in rich_item:
                                    rich_item_dict[j] = rich_item[j]



                                #Overwriting the default Field
                                if urlparts.query:
                                    queryparts = urlparts.query.split('&')
                                    print('queryparts:',queryparts)
                                    for querypart in queryparts:
                                        paramparts = querypart.split('=')
                                        print('paramparts:',paramparts)
                                        if paramparts[0]=='fl':
                                            flparts = paramparts[1].split(',')
                                            print('flparts:',flparts)   
                                            external_FieldName = flparts[0]
                                #The value for the Field picked (or the first Field if default)
                                value = rich_item[external_FieldName]

                                print('value:',value)

                                print('rich_item_dict:',rich_item_dict)


                                old_value = item.items[0][field['FieldName']]
                                item.items[0][field['FieldName']] = value
                                item.rich[0][field['FieldName']] = rich_item_dict


                                #RECORD THIS PATCH HISTORY

                                history_item = {}
                                history_item['date'] = str(datetime.now())
                                history_item['author'] = handle
                                history_item['before'] = old_value
                                history_item['after'] = value
                                history_item['action'] = 'Patch p20150113'
                                item.history[0][field['FieldName']].append(history_item)
                         

                    else:
                        #Not a select. Will not have rich data
                        print(field['FieldName']+' is NOT a RICH Field ')
                        



                if needs_saving:
                    if item.store(db): 
                        print('item document saved:',item)
                else:
                    print('Nothing to patch here')   

        else:
            print('Please indicate this in URL:  ?handle=x&ringname=y')  
                

        d = {'rq': current_user,'template':'avispa_rest/tools/flashresponsejson.html'}
        return d

    def p20150128(self,request,*args):
        '''
        This patch runs authmodel.userdb_set_db_views() to create the new userdatabase views : 
        '''

        from auth.AuthModel import AuthModel

        ATM = AuthModel()

        ATM.userdb_set_db_views()

        d = {'rq': 'ok','template':'avispa_rest/tools/flashresponsejson.html'}
        return d

        


























