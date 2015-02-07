# AvispaModel.py
from couchdb.http import PreconditionFailed, ResourceNotFound

from datetime import datetime 
import time
import datetime as dt
import random
import sys
import requests
import urlparse
import json

import traceback
import collections
from flask import flash
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField, Mapping 
from couchdb.design import ViewDefinition
from couchdb.http import ResourceNotFound
from MyRingSchema import MyRingSchema
from CouchViewSync import CouchViewSync

from MyRingCouchDB import MyRingCouchDB
from MyRingUser import MyRingUser
from MainModel import MainModel
from env_config import COUCHDB_USER, COUCHDB_PASS


class AvispaModel:


    def __init__(self):

        MCD = MyRingCouchDB()
        self.couch=MCD.instantiate_couchdb_as_admin()    
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        #print('self.couch :AVM')
        #print(self.couch)
        #print('self.couch.resource.credentials :AVM')
        #print(self.couch.resource.credentials)
        self.user_database = 'myring_users'



        self.MAM = MainModel()
 

    #AVISPAMODEL
    def user_get_rings(self,handle,user_database=None):


        if not user_database : 
            user_database = self.user_database


        data=[]

        try:
                   
            db = self.MAM.select_db(user_database)
            
            user_doc = self.MAM.select_user(user_database,handle)
            
            rings = user_doc['rings']
            
            print(rings)
         

            for ring in rings:
                
                if not 'deleted' in ring:
                    
                    ringname = str(ring['ringname'])
                    ringversion = str(ring['version'])
                    if 'origin' in ring:
                        ringorigin = str(ring['origin'])
                    else:
                        ringorigin = str(handle)

                    ringversionh = ringversion.replace('-','.')
                    count = ring['count']
                    #print('flag5b:'+str(handle)+'_'+ringname+'_'+ringversion)
                    print('flag5b:'+str(handle)+'_'+ringname)
                    #ringnamedb=str(handle)+'_'+ringname+'_'+ringversion
                    ringnamedb=str(handle)+'_'+ringname
                    print('ringnamedb::'+ringnamedb) 
                    try:
                        db = self.MAM.select_db(ringnamedb)
                        print('Get RingDescription:')
                        try: 
                            RingDescription = db['schema']['rings'][0]['RingDescription'] 
                        except KeyError:
                            RingDescription = False 
                        
                        print('Get RingLabel:')
                        try:       
                            RingLabel = db['schema']['rings'][0]['RingLabel'] 
                        except KeyError:
                            RingLabel = False 

                        r = {
                            'ringname':ringname,
                            'ringversion':ringversion,
                            'ringversionh':ringversionh,
                            'ringorigin':ringorigin,
                            'ringlabel':RingLabel,
                            'ringdescription':RingDescription,
                            'count':count}

                        data.append(r)
                    except ResourceNotFound:
                        #print('skipping ring '+ ringname+'_'+ringversion + '. Schema does not exist')
                        print('skipping ring '+ ringname + '. Schema does not exist')
                        

            #print('flag6')

            

        except (ResourceNotFound, TypeError) as e:

            #BUG: This exception gets triggered even if the ring does exist
            #The problem has to do with pagination. It can't find it in the current page

            #flash("You have no rings yet, create one!")
            print "Notice: Expected error:", sys.exc_info()[0] , sys.exc_info()[1]
            #print('Notice: No rings for this user.')

        return data


    #AVISPAMODEL
    def ring_set_db(self,handle,ringname,ringversion):
           
        #db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db_ringname=str(handle)+'_'+str(ringname)
        db_ringname = db_ringname.replace(" ","")

        try:            
            #self.couch.create(db_ringname) #Creates this ring database
            self.MAM.create_db(db_ringname)
            self.ring_set_db_views(db_ringname) #Sets all the CouchDB Views needed for this new ring
            self.user_add_ring(handle,ringname,ringversion) #Adds the ring to the user's list
            return True    

        except:
            print "Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1]
            #flash(u'Unexpected error:'+ str(sys.exc_info()[0]) + str(sys.exc_info()[1]),'error')
            self.rs_status='500'
            raise


            return False


    #AVISPAMODEL
    def x_ring_set_db_views(self,db_ringname): 
    #Implemented as indicated here: http://markhaase.com/2012/06/23/couchdb-views-in-python/
    #Deprecated. Only useful if view function are in python. 
    #Python + CouchDB very poor and complicated as of now. 
    #I rather use JS in the meantime


        db = self.couch[db_ringname]

        CVS = CouchViewSync()
        return CVS.set_db_views(db)

    #AVISPAMODEL
    def ring_set_db_views(self,db_ringname,specific=False):

        db = self.couch[db_ringname]

        
        if not specific or specific == 'ring/items':
            view = ViewDefinition('ring', 'items', 
                   '''
                      function(doc) {
                        if(doc.items) {
                           if(!doc.deleted) {
                              var x = new Object();  
                              x['_public']=doc.public
                              for (var key in doc.items[0]) { 
                                 x[key]=doc.items[0][key]; 
                              }
                              emit(doc._id, x)
                           }
                        }
                      }
                   ''')

            view.get_doc(db)
            view.sync(db)

        if not specific or specific == 'ring/rich':
            view = ViewDefinition('ring', 'rich', 
                   '''
                      function(doc) {
                        if(doc.rich) {
                           if(!doc.deleted) {
                              var x = new Object();  
                              x['_public']=doc.public
                              for (var key in doc.rich[0]) { 
                                 x[key]=doc.rich[0][key]; 
                              }
                              emit(doc._id, x)
                           }
                        }
                      }
                   ''')

            view.get_doc(db)
            view.sync(db)

        if not specific or specific == 'ring/history':
            view = ViewDefinition('ring', 'history', 
                   '''
                      function(doc) {
                        if(doc.history) {
                           if(!doc.deleted) {
                              var x = new Object();  
                              x['_public']=doc.public
                              for (var key in doc.history[0]) { 
                                 x[key]=doc.history[0][key]; 
                              }
                              emit(doc._id, x)
                           }
                        }
                      }
                   ''')

            view.get_doc(db)
            view.sync(db)


        if not specific or specific == 'ring/meta':
            view = ViewDefinition('ring', 'meta', 
                   '''
                      function(doc) {
                        if(doc.meta) {
                           if(!doc.deleted) {
                              var x = new Object();  
                              x['_public']=doc.public
                              for (var key in doc.meta[0]) { 
                                 x[key]=doc.meta[0][key]; 
                              }
                              emit(doc._id, x)
                           }
                        }
                      }
                   ''')

            view.get_doc(db)
            view.sync(db)

        if not specific or specific == 'item/roles':
            view = ViewDefinition('item', 'roles', 

                   '''
                    function(doc) {
                        if(doc.history) {
                            if(!doc.deleted) {
                                var x = new Object();  
                                x['_public']=doc.public
                                for (var key in doc.roles) { 
                                   x[key]=doc.roles[key]; 
                                }
                            emit(doc._id, x)
                            }
                        }
                    }
                   ''')

            view.get_doc(db)
            view.sync(db)


        if not specific or specific == 'ring/schema':
            view = ViewDefinition('ring', 'schema', 
                   '''
                    function(doc) {
                      if(doc._id=='schema'){   
                        emit(doc._id, doc)
                      }
                    }
                   ''')

            view.get_doc(db)
            view.sync(db)

        return True


    #AVISPAMODEL
    def user_add_ring(self,handle,ringname,ringversion,user_database=None):

        if not user_database : 
            user_database = self.user_database

        db = self.couch[user_database]
        print("handle:")
        print(handle)
        doc =  MyRingUser.load(db, handle)
        doc.rings.append(ringname=str(ringname),version=str(ringversion),added=datetime.now(),count=0)
        doc.store(db)

        return True

    #AVISPAMODEL
    def user_delete_ring(self,handle,ringname,user_database=None):

        db = self.couch[self.user_database]
        doc =  MyRingUser.load(db, handle)
        rings = doc['rings']
        for ring in rings:
            if ring['ringname']==ringname:
                print()
                ring['deleted']=True
                #It is just a tombstone!!
                

        if doc.store(db):
            return True

        #doc.rings.append(ringname=str(ringname),version=str(ringversion),added=datetime.now(),count=0)
        #doc.store(db)
        
        return False

    #AVISPAMODEL
    def user_hard_delete_ring(self,handle,ringname,ringversion,user_database=None):

        #dbname = handle+'_'+ringname+'_'+ringversion
        dbname = handle+'_'+ringname
        if self.MAM.delete_db(dbname):
            print('Deleted from COUCHDB')
            del1 = True


        db = self.couch[self.user_database]
        doc =  MyRingUser.load(db, handle)
        rings = doc['rings']
        for ring in rings:
            if ring['ringname']==ringname and ring['version']==ringversion:
                
                ring['deleted']=True
                
        if doc.store(db):
            print('Deleted from USERDB')
            del2 = True
      

        if del1 and del2:
            return True
        else:
            return False

    #AVISPAMODEL
    def ring_get_schema(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        print(db_ringname)
        db = self.couch[db_ringname]
        schema = MyRingSchema.load(db,'schema')

        return schema


    #AVISPAMODEL
    def ring_get_item_document(self,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)

        return item

        



    #AVISPAMODEL
    def ring_set_schema(self,handle,ringname,ringversion,pinput,ringprotocol,fieldprotocol):

        
        if ringversion == 'None' or ringversion == None:
            print('ringversion none')
            ringversion = ''

        #db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db_ringname=str(handle)+'_'+str(ringname)
        print('db_ringname:')
        print(db_ringname)
        db = self.couch[db_ringname]
        numfields = len(pinput['fields'])
        schema = MyRingSchema.load(db,'schema')

        # Creates Ring Schema if it doesn't exist. Uses current one if it exists.
        if schema:
            action = 'edit'
        else:       
            schema = MyRingSchema()
            #ring = RingClass()
            schema._id= 'schema'

            action = 'new'


        # Creates or updates Shcema parameters

        args_r = {}
        for r in ringprotocol:
            if(action == 'new'):
                #if r in schema.rings[0]:
                if pinput['rings'][0][r]:
                    args_r[r] = pinput['rings'][0][r]
            
            elif(action == 'edit'):
                if r in schema.rings[0]:
                    if pinput['rings'][0][r] == schema.rings[0][r]:
                        print(r+' did not change')
                        
                    else:
                        print(r+' changed. Old: "'+ str(schema.rings[0][r]) +'" ('+ str(type(schema.rings[0][r])) +')'+\
                                '  New: "'+ str(pinput['rings'][0][r]) + '" ('+ str(type(pinput['rings'][0][r])) +')' )
                        args_r[r] = pinput['rings'][0][r]

                  

        
        if(action == 'new'):
            schema.rings.append(**args_r)
        
        elif(action == 'edit'):
            for x in args_r:
                schema.rings[0][x] = args_r[x]
            

        # Creates or updates Field parameters

        args_f = {}


        for i in xrange(0,numfields):
            for f in fieldprotocol:

                #Boolean correction
                if pinput['fields'][i][f] == 'FALSE':
                    pinput['fields'][i][f] = False
                elif pinput['fields'][i][f] == 'TRUE':
                    pinput['fields'][i][f] = True
                

                if(action == 'new'):
                    if pinput['fields'][i][f] or pinput['fields'][i][f]==False:  #BUG Aqui deberia leer False as 'False'!!!      
                        args_f[f] = pinput['fields'][i][f]

                elif(action == 'edit'):
                    if pinput['fields'][i][f] == schema.fields[i][f]:  # Checks if old and new are the same
                        print(f+'_'+str(i+1)+' did not change')
                    else:                      
                        print(f+'_'+str(i+1)+' changed. Old: "'+ str(schema.fields[i][f]) +'" ('+ str(type(schema.fields[i][f])) +')'+\
                            '  New: "'+ str(pinput['fields'][i][f]) + '" ('+ str(type(pinput['fields'][i][f])) +')' )
                        
                        args_f[f] = pinput['fields'][i][f]


            #print('args_f:')
            #print(args_f)

            if(action == 'new'):
                schema.fields.append(**args_f)
                
            elif(action == 'edit'):
                for y in args_f:
                    schema.fields[i][y] = args_f[y]

            args_f={}

        print(schema)

        
        schema.store(db)

        return 'ok'

    
    #AVISPAMODEL
    def _schema_create_class(self,numfields,ringprotocol,fieldprotocol):
        '''
        This function is deprecated. Now we just instantiate MyRingSchema class
        '''

        args_r = {}
        args_f = {} 

        for r in ringprotocol:

            args_r[r] = TextField()

        for i in xrange(1,numfields):

            for f in fieldprotocol:

                args_f[f] =  TextField()


        schemaclass = type('SchemaClass',
                         (Document,),
                         {
                            '_id' : TextField(),

                            'rings': ListField(DictField(Mapping.build(
                                                    **args_r
                                                ))),
                            'fields':ListField(DictField(Mapping.build(
                                                    **args_f
                                                )))
                                               })

        return schemaclass

    
    #AVISPAMODEL
    def ring_create_class(self,schema):

        args_i = {}
        args_rich = {}
        args_history = {}
        args_meta = {}

        fields = schema['fields']
        for field in fields:
            args_i[field['FieldName']] = TextField()

            #d1={'source':TextField()}
            d1 = {}
            d1['source']=TextField()
            print('len:',len(d1))
            args_rich[field['FieldName']] = DictField()

            d2 = {}
            d2['date']=DateTimeField()
            d2['author']=TextField()
            d2['before']=TextField()
            d2['after']=TextField()
            args_history[field['FieldName']] = ListField(DictField(Mapping.build(**d2)))
            
            args_meta[field['FieldName']] = DictField()
            


        print('args_i',args_i)
        print('args_rich',args_rich)
        print('args_history',args_history)
        print('args_meta',args_meta)

 

        RingClass = type('RingClass',
                         (Document,),
                         {
                            '_id' : TextField(),
                            'added' : DateTimeField(default=datetime.now()),
                            'license' : TextField(),
                            'public' : BooleanField(default=False),
                            'deleted' : BooleanField(default=False),
                            'items': ListField(DictField(Mapping.build(
                                                    **args_i
                                                ))),
                            'rich': ListField(DictField(Mapping.build(
                                                    **args_rich
                                                ))),
                            'history': ListField(DictField(Mapping.build(
                                                    **args_history
                                                ))),
                            'meta': ListField(DictField(Mapping.build(
                                                    **args_meta
                                                )))
                                               }) 

        print('RingClass:',RingClass)

        return RingClass


    #AVISPAMODEL
    def get_item_count(self,handle,ringname,user_database=None):


        if not user_database : 
            user_database = self.user_database

        user_doc = self.MAM.select_user(user_database,handle)
        print('user rings:',user_doc['rings'])
        for user_ring in user_doc['rings']:
            if user_ring['ringname']==ringname:
                return user_ring['count']


        return False


    #AVISPAMODEL
    def increase_item_count(self,handle,ringname):

        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:

            for ring in user['rings']:
                if ring['ringname'] == ringname:
                    ring['count'] += 1
                    print('Item Count increased')

            if user.store(self.db):
                
                return True
            else:
                print('Could not increase item count')
                return False

    def set_ring_origin(self,handle,ringname,origin):

        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:

            for ring in user['rings']:
                if ring['ringname'] == ringname:

                    ring['origin'] = origin
                    print('Ring origin set to '+origin)

            if user.store(self.db):
                
                return True
            else:
                print('Could not set origin')
                return False



    #AVISPAMODEL
    def ring_get_schema_from_view(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        print(db_ringname)
        db = self.couch[db_ringname]

        options = {}
        result  = db.iterview('ring/schema',1,**options)

        for row in result:  
            #print('row.value.fields:')
            #print(row.value['fields'])    
            schema = {}
            #schema['rings']=row.value
            schema['fields']=row.value['fields']
            schema['rings']=row.value['rings']
            #schema['rings']=row.rings
            #schema['fields']=row.fields

        #print('schema:')
        #print(schema)

        return schema

        #return False


    #AVISPAMODEL
    def couchdb_pager(db, view_name='_all_docs',
                  startkey=None, startkey_docid=None,
                  endkey=None, endkey_docid=None, bulk=5000):

        '''
        import couchdb
        couch = couchdb.Server()
        db = couch['mydatabase']

        # This is dangerous.
        for doc in db:
            pass

        # This is always safe.
        for doc in couchdb_pager(db):
            pass

        '''
        # Request one extra row to resume the listing there later.
        options = {'limit': bulk + 1}
        if startkey:
            options['startkey'] = startkey
            if startkey_docid:
                options['startkey_docid'] = startkey_docid
        if endkey:
            options['endkey'] = endkey
            if endkey_docid:
                options['endkey_docid'] = endkey_docid
        done = False
        while not done:
            view = db.view(view_name, **options)
            rows = []
            # If we got a short result (< limit + 1), we know we are done.
            if len(view) <= bulk:
                done = True
                rows = view.rows
            else:
                # Otherwise, continue at the new start position.
                rows = view.rows[:-1]
                last = view.rows[-1]
                options['startkey'] = last.key
                options['startkey_docid'] = last.id

            for row in rows:
                yield row.id


    

    def get_a_b_parameters(self,handle,ringname,user_database=None):
        
        if not user_database : 
            user_database = self.user_database

        user_doc = self.MAM.select_user(user_database,handle)

        print('user rings:',user_doc['rings'])
        for user_ring in user_doc['rings']:
            if user_ring['ringname']==ringname:
                parameters = {}
                parameters['count'] = user_ring['count']
                if 'origin' in user_ring:
                    parameters['ringorigin'] = user_ring['origin']
                else:
                    parameters['ringorigin'] = handle

                
                return parameters


        return False


    

    #AVISPAMODEL
    def get_a_b(self,handle,ringname,limit=100,lastkey=None,sort=None):



        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]
        batch = 500  #This is not the number of results per page. 
         # https://pythonhosted.org/CouchDB/client.html#couchdb.client.Database.iterview

        schema = self.ring_get_schema_from_view(handle,ringname) 
        OrderedFields=[]
        for field in schema['fields']:
            OrderedFields.insert(int(field['FieldOrder']),field['FieldName'])


        sort_reverse=False
        if sort:
            sort_parts = sort.split('_')
            if len(sort_parts)==2:
                if sort_parts[1].lower()=='desc':
                    sort_reverse=True

                sort= sort_parts[0]

        else:
            sort = OrderedFields[0]
            

        #print('schema:')
        #print(schema)

        #print('OrderedFields:')
        #print(OrderedFields)

        options = {}
        if lastkey:
            limit +=1
            options['startkey']=lastkey  #Where the last page left

        options['limit']=limit #Number of results per page
        
        
        #options['key']='4393588627'
        
        #options['startkey_docid']='4393588627'
        #options['endkey']='4393588626'
        #options['endkey_docid']=4


        result = db.iterview('ring/items',batch,**options)

        #print ('ITEMS FROM VIEW:',result)

        presorteditems = []
        for row in result:
            presorteditems.append(row)

        #print('PRESORTEDITEMS:', presorteditems)

        items = []
        i = 0

        for row in presorteditems:

            i += 1
            if lastkey and i==1:
                #If lastkey was sent, ignore first item 
                #as it was the last item in the last page
                #print('length:')
                #print(len(items))
                continue
                #pass

            #item = {} #Make this an ordered dictionary
            #This will output the fields as specified in the schema
            item = collections.OrderedDict()

            item[u'_id'] = row['id']

            for fieldname in OrderedFields:
                if fieldname in row['value']:
                    item[fieldname] = row['value'][fieldname]

            #item.update(row['value'])

            #item['id']=row['id']
            #item['values']=row['value']
            items.append(item)
            #print("item:")
            #print(item)
            
            #sort = 'Dificultad'

            
            #self.sort=sort
            #print('Sorting by '+sort)
            self.sort = sort
            items = sorted(items, key=self.SortItemList, reverse=sort_reverse)
        #print(items)

        return items

    def SortItemList(self,items):
        if self.sort:
            return items[self.sort]
        else:
            return items[1:]





    #AVISPAMODEL
    def post_a_b(self,request,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        
        item_values = {}
        rich_values = {}
        history_values = {}
        fields = schema['fields']

        print("post_a_b raw arguments sent:")
        print(request.form)


        for field in fields:
            

            print(field['FieldName']+' content: '+str(request.form.get(field['FieldName'])))
            print(field['FieldName']+' type: '+str(type(request.form.get(field['FieldName']))))

            print('FieldSource:',field['FieldSource'])
            print('FieldWidget:',field['FieldWidget'])

            #Detect if FieldWidget is "select" . If it is you are getting an ID. 
            #You need to query the source to get the real value and the _rich values
            if field['FieldSource'] and field['FieldWidget']=='select' and len(request.form.get(field['FieldName']))!=0:
                print(field['FieldName']+' is a RICH Field ')
                external_id=int(request.form.get(field['FieldName'])) #need to sanitize this more
                print('external_id',external_id)
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

                    rich_item = self.get_a_b_c(None,external_handle,external_ringname,external_id)

                    rs = self.ring_get_schema_from_view(external_handle,external_ringname)

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
                
                item_values[field['FieldName']] = value
                rich_values[field['FieldName']] = rich_item_dict
               
 
            else:
                #Not a select. Will not have rich data
                print(field['FieldName']+' is NOT a RICH Field ')
                item_values[field['FieldName']] = request.form.get(field['FieldName'])


            
            #This will record the history for the first entry in the item history
            history_item = {}
            history_item['date'] = datetime.now()
            history_item['author'] = handle
            history_item['before'] = ''
            history_item['after'] = item_values[field['FieldName']]

            history_list = []
            history_list.append(history_item)

            history_values[field['FieldName']] = history_list


        RingClass = self.ring_create_class(schema)
        item = RingClass()        
        item._id= str(random.randrange(1000000000,9999999999))
        #item.deleted = 
        item.items.append(**item_values)
        print("rich_values:",rich_values)
        #item.rich.append(**rich_values)
        item.rich.append(**rich_values)
        item.history.append(**history_values)
        
        
        if item.store(db):
        
            self.increase_item_count(handle,ringname)

            return item._id

        return False


    #AVISPAMODEL
    def get_a_b_c(self,request,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        print('db_ringname:',db_ringname)
        db = self.couch[db_ringname]
        print('db:',db)

        schema = self.ring_get_schema_from_view(handle,ringname)   
        OrderedFields=[]
        for field in schema['fields']:
            #print("order:FieldName")
            #print(field['FieldOrder'],field['FieldName'])
            OrderedFields.insert(int(field['FieldOrder']),field['FieldName'])
        
        print('OrderedFields:',OrderedFields)
        print('idx:',idx)

        
        options = {}
        options['key']=str(idx)

        #Retrieving from ring/items view
        result = db.iterview('ring/items',1,**options)

        print('result:',result)

        
        for row in result:      
            item = collections.OrderedDict()
            print('row',row)
            if row['id']:        
                item[u'_id'] = row['id']

                for fieldname in OrderedFields:
                    item[fieldname] = row['value'][fieldname]
                    #item.update(row['value'])

                print("item:")
                return item

        return False


    #AVISPAMODEL
    def put_a_b_c(self,request,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)
        
        item_values = {}
        history_values = {}
        fields = schema['fields']

        if request.form.get('_public'):
            item['public']=True
        else:
            item['public']=False

        for field in fields:
            #item_values[field['FieldName']] = request.form.get(field['FieldName']) #aquire all the data coming via POST
            f = field['FieldName']
            old = unicode(item.items[0][f])
            new = unicode(request.form.get(f))

            #old = old.strip()
            new = new.strip()

            if old == new:
                print(f+' did not change')             
            else:
                print(f+' changed. Old: "'+ str(old) +'" ('+ str(type(old)) +')'+\
                                '  New: "'+ str(new) + '" ('+ str(type(new)) +')' )
                #args[f] = new
                item.items[0][f] = new

                #This will record the history for the item update 
                history_item = {}
                history_item['date'] = str(datetime.now())
                history_item['author'] = handle
                history_item['before'] = str(old) +' '+ str(type(old)) 
                history_item['after'] = str(new) + ' '+ str(type(new))
                
                #history_list = item.history[0][field['FieldName']]
                #history_list.append(**history_item)

                #history_values[field['FieldName']] = history_list

                #item.history[0][field['FieldName']].append(**history_item)
                '''
                if history not in item:
                    item['history'] = []

                if not item.history[0]:

                    fields = {}

                    item.history.append
                '''

                item.history[0][field['FieldName']].append(history_item)

        if item.store(db):      
            return item._id

        return False



        ''' Optional way to retrieve from DB (not view)

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)

        item = RingClass.load(db,idx)
        item['items'][0][u'id']=idx


        #return item['items'][0]
        '''

    def delete_a_b_c(self,request,handle,ringname,idx):


        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)
        
        '''
        item_values = {}
        fields = schema['fields']
        for field in fields:
            #values[field['FieldName']] = request.form.get(field['FieldName']) #aquire all the data coming via POST
            f = field['FieldName']
            old = unicode(item.items[0][f])
            new = unicode(request.form.get(f))

            if old == new:
                print(f+' did not change')             
            else:
                print(f+' changed. Old: "'+ str(old) +'" ('+ str(type(old)) +')'+\
                                '  New: "'+ str(new) + '" ('+ str(type(new)) +')' )
                #args[f] = new
                item.items[0][f] = new
        '''

        item.deleted = True

        if item.store(db): 

            return item._id

        return False




    