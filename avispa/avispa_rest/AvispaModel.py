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
import logging
import couchdb

from flask import flash, current_app, g
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField, Mapping 
from couchdb.design import ViewDefinition
from couchdb.http import ResourceNotFound
from MyRingSchema import MyRingSchema
from AvispaLogging import AvispaLoggerAdapter



from MyRingUser import MyRingUser
from MainModel import MainModel
from env_config import COUCHDB_SERVER, COUCHDB_USER, COUCHDB_PASS

from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)



class AvispaModel:


    def __init__(self):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': g.get('tid', None),'ip': g.get('ip', None)})

        self.lggr.info('__init__()')
  
        #current_app.logger.debug('#couchdb_call')
        self.couch = couchdb.Server(COUCHDB_SERVER)
        self.couch.resource.credentials = (COUCHDB_USER,COUCHDB_PASS)
        ##current_app.logger.debug('self.couch :AVM')
        #current_app.logger.debug(self.couch)
        #current_app.logger.debug('self.couch.resource.credentials :AVM')
        #current_app.logger.debug(self.couch.resource.credentials)
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
            
            #current_app.logger.debug(rings)
         

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
                    #current_app.logger.debug('flag5b:'+str(handle)+'_'+ringname+'_'+ringversion)
                    #current_app.logger.debug('flag5b:'+str(handle)+'_'+ringname)
                    #ringnamedb=str(handle)+'_'+ringname+'_'+ringversion
                    ringnamedb=str(handle)+'_'+ringname
                    #current_app.logger.debug('ringnamedb::'+ringnamedb) 
                    try:
                        db = self.MAM.select_db(ringnamedb)
                        #current_app.logger.debug('Get RingDescription:')
                        try: 
                            RingDescription = db['schema']['rings'][0]['RingDescription'] 
                        except KeyError:
                            RingDescription = False 
                        
                        #current_app.logger.debug('Get RingLabel:')
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
                        pass
                        
                        self.lggr.info('skipping ring '+ ringname + '. Schema does not exist')
                        

            #current_app.logger.debug('flag6')

            

        except (ResourceNotFound, TypeError) as e:

            #BUG: This exception gets triggered even if the ring does exist
            #The problem has to do with pagination. It can't find it in the current page

            #flash("You have no rings yet, create one!")
            self.lggr.info("Notice: Expected error:", sys.exc_info()[0] , sys.exc_info()[1])
            #current_app.logger.debug('Notice: No rings for this user.')

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
            current_app.logger.error ("Unexpected error:", sys.exc_info()[0] , sys.exc_info()[1])
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

        current_app.logger.debug('#couchdb_call')
        db = self.couch[db_ringname]

        CVS = CouchViewSync()
        return CVS.set_db_views(db)

    #AVISPAMODEL
    def ring_set_db_views(self,db_ringname,specific=False):

        current_app.logger.debug('#couchdb_call')
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
                            for (var key in doc.rich[0]) { 
                               if(doc.rich[0][key].length!=0){
                                  x[key+'_rich']=doc.rich[0][key]; 
                               }
                            }
                            if(doc.flags){
                               for (var key in doc.flags[0]) { 
                                  x[key+'_flag']=doc.flags[0][key]; 
                               }
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

        if not specific or specific == 'ring/dailyactivity':
            view = ViewDefinition('ring', 'dailyactivity', 
                   '''
                    function(doc) {
                      if(doc.history) {
                         if(!doc.deleted) {
                            var c = new Object(); 
                            
                            for (var key in doc.history[0]) {           
                               for (var h in doc.history[0][key]){ 
                                   var author = doc.history[0][key][h]['author'];
                                   var action = doc.history[0][key][h]['action'];
                                   var date = doc.history[0][key][h]['date'].substring(0,10);
                                   var before = doc.history[0][key][h]['before']
                                   var after = doc.history[0][key][h]['after']
                                   
                                   if(!(author in c)){               
                                       var a = new Object();
                                       a['new'] = new Object();
                                       a['update'] = new Object();                
                                       c[author] = a;
                                   }

                                   if(doc.history[0][key][h]['action'] == 'New item'){                
                                       if(!(date in c[author]['new'])){
                                           c[author]['new'][date] = 0;
                                       }
                                       if(before != after){
                                           c[author]['new'][date] += 1;
                                       }
                                   }else if(doc.history[0][key][h]['action'] == 'Update item'){              
                                       if(!(date in c[author]['update'])){
                                           c[author]['update'][date] = 0;
                                       }
                                       c[author]['update'][date] += 1;
                                   }                              
                               }
                            }
                            for(ax in c){
                                emit(ax, c[ax]); 
                            }       
                         }
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

        current_app.logger.debug('#couchdb_call')
        db = self.couch[user_database]
        
        self.lggr.info("handle:",handle)
        doc =  MyRingUser.load(db, handle)
        doc.rings.append(ringname=str(ringname),version=str(ringversion),added=datetime.now(),count=0)
        doc.store(db)

        return True

    #AVISPAMODEL
    def user_delete_ring(self,handle,ringname,user_database=None):

        if not user_database : 
            user_database = self.user_database

        current_app.logger.debug('#couchdb_call')
        db = self.couch[user_database]
        doc =  MyRingUser.load(db, handle)
        

        #Clean all the references to this ring in the user document
        # This is NOT a tombstone. The database and its data will be deleted. 
        # TO DO : Backup the data in a secondary database
        self.lggr.info('Looking for ring '+ringname+' in the ringlist for this user')
        i = 0
        for ring in doc['rings']:
            
            if ring['ringname']==ringname:
                self.lggr.info('Found it!... Deleting it')
                self.lggr.info("doc['rings']["+str(i)+"]")
                del doc['rings'][i]
                #current_app.logger.debug()
                #ring['deleted']=True           
                # This is NOT a tombstone. The database and its data will be deleted. 
                # TO DO : Backup the data in a secondary database
                try:
                    self.lggr.info('Try to Delete DB')
                    if self.MAM.delete_db(handle+'_'+ringname):
                        self.lggr.info('DB Deleted')
                except:
                    self.lggr.info('DB already does not exist. Deleting all its references')    
            i = i+1

        j = 0
        for collection in doc['collections']:
            self.lggr.info('Looking in collection '+collection['collectionname']+' for this ring')
            k = 0
            for ring in collection['rings']:
                if ring['ringname']==ringname:
                    self.lggr.info('Found it! ... Deleting it'+ str(j)+'-')
                    self.lggr.info("doc['collections']["+str(j)+"]['rings']["+str(k)+"]")
                    del doc['collections'][j]['rings'][k]

                k = k+1

            j = j+1
                
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
            self.lggr.info('Deleted from COUCHDB')
            del1 = True


        current_app.logger.debug('#couchdb_call')
        db = self.couch[self.user_database]
        user_doc =  MyRingUser.load(db, handle)
        rings = user_doc['rings']
        count = 0
        for ring in rings:
            if ring['ringname']==ringname and ring['version']==ringversion:
                #Here you should also make a hard delete not only a tombstone
                del user_doc['rings'][count]

            count += 1

                #ring['deleted']=True
                
        if user_doc.store(db):
            self.lggr.info('Deleted from USERDB')
            del2 = True
      

        if del1 and del2:
            return True
        else:
            return False

    #AVISPAMODEL
    def ring_get_schema(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        
        current_app.logger.debug('#couchdb_call:'+db_ringname+'->ring_get_schema()')

        db = self.couch[db_ringname]
        schema = MyRingSchema.load(db,'schema')

        return schema


    #AVISPAMODEL
    def ring_get_item_document(self,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        current_app.logger.debug('#couchdb_call')
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)

        return item

        



    #AVISPAMODEL
    def ring_set_schema(self,handle,ringname,ringversion,pinput,ringprotocol,fieldprotocol):

        
        if ringversion == 'None' or ringversion == None:
            self.lggr.info('ringversion none')
            ringversion = ''

        #db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db_ringname=str(handle)+'_'+str(ringname)
        
        current_app.logger.debug('db_ringname:'+str(db_ringname))
        current_app.logger.debug('#couchdb_call')
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


        # Creates or updates Schema parameters

        args_r = {}
        for r in ringprotocol:
            if(action == 'new'):
                #if r in schema.rings[0]:
                if r in pinput['rings'][0]:
                    args_r[r] = pinput['rings'][0][r]
            
            elif(action == 'edit'):
                if r in schema.rings[0]:
                    if pinput['rings'][0][r] == schema.rings[0][r]:
                        self.lggr.info(r+' did not change')
                        
                    else:
                        self.lggr.info(r+' changed. Old: "'+ str(schema.rings[0][r]) +'" ('+ str(type(schema.rings[0][r])) +')'+\
                                '  New: "'+ str(pinput['rings'][0][r]) + '" ('+ str(type(pinput['rings'][0][r])) +')' )
                        args_r[r] = pinput['rings'][0][r]

                  

        
        if action == 'new':
            schema.rings.append(**args_r)
        
        elif action == 'edit':
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

                if action == 'new':
                    if pinput['fields'][i][f] or pinput['fields'][i][f]==False:  #BUG Aqui deberia leer False as 'False'!!!      
                        args_f[f] = pinput['fields'][i][f]

                elif action == 'edit':
                    if pinput['fields'][i][f] == schema.fields[i][f]:  # Checks if old and new are the same
                        self.lggr.info(f+'_'+str(i+1)+' did not change')
                    else:                      
                        self.lggr.info(f+'_'+str(i+1)+' changed. Old: "'+ str(schema.fields[i][f]) +'" ('+ str(type(schema.fields[i][f])) +')'+\
                            '  New: "'+ str(pinput['fields'][i][f]) + '" ('+ str(type(pinput['fields'][i][f])) +')' )
                        
                        args_f[f] = pinput['fields'][i][f]


            #current_app.logger.debug('args_f:')
            #current_app.logger.debug(args_f)

            if action == 'new':
                args_f['FieldId'] = self.MAM.random_hash_generator(36)

                schema.fields.append(**args_f)
                
            elif action == 'edit' :

                if 'FieldId' not in schema.fields[i]:
                    args_f['FieldId'] = self.MAM.random_hash_generator(36)

                for y in args_f:
                    schema.fields[i][y] = args_f[y]

            args_f={}

        current_app.logger.debug(schema)

        
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
        args_flags = {}

        fields = schema['fields']
        for field in fields:
            args_i[field['FieldId']] = TextField()

            #d1={'source':TextField()}
            d1 = {}
            d1['_id']=TextField()
            d1['_source']=TextField()
            current_app.logger.debug('len:'+str(len(d1)))
            args_rich[field['FieldId']] = ListField(DictField())
            

            d2 = {}
            d2['date']=DateTimeField()
            d2['author']=TextField()
            d2['before']=TextField()
            d2['after']=TextField()
            d2['action']=TextField()
            d2['doc']=DictField()
            args_history[field['FieldId']] = ListField(DictField(Mapping.build(**d2)))

            args_flags[field['FieldId']] = TextField()

            args_meta[field['FieldId']] = DictField()


            


        current_app.logger.debug('args_i'+str(args_i))
        current_app.logger.debug('args_rich'+str(args_rich))
        current_app.logger.debug('args_history'+str(args_history))
        current_app.logger.debug('args_flags'+str(args_flags))
        current_app.logger.debug('args_meta'+str(args_meta))

 

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
                            'flags': ListField(DictField(Mapping.build(
                                                    **args_flags
                                                ))),
                            'meta': ListField(DictField(Mapping.build(
                                                    **args_meta
                                                )))
                                               }) 

        self.lggr.info('RingClass:'+str(RingClass))

        return RingClass


    #AVISPAMODEL
    def get_item_count(self,handle,ringname,user_database=None):


        if not user_database : 
            user_database = self.user_database

        user_doc = self.MAM.select_user(user_database,handle)
        self.lggr.info('user rings:'+str(user_doc['rings']))
        for user_ring in user_doc['rings']:
            if user_ring['ringname']==ringname:
                return user_ring['count']


        return False


    #AVISPAMODEL
    def increase_item_count(self,handle,ringname):

        current_app.logger.debug('#couchdb_call')
        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:

            for ring in user['rings']:
                if ring['ringname'] == ringname:
                    ring['count'] += 1
                    self.lggr.info('Item Count increased')

            if user.store(self.db):
                
                return True
            else:
                current_app.logger.error('Could not increase item count')
                return False

        #AVISPAMODEL
    def decrease_item_count(self,handle,ringname):

        current_app.logger.debug('#couchdb_call')
        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:
            for ring in user['rings']:
                if ring['ringname'] == ringname:
                    ring['count'] -= 1
                    self.lggr.info('Item Count decreased')

            if user.store(self.db):       
                return True
            else:
                current_app.logger.error('Could not decrease item count')
                return False

    def set_ring_origin(self,handle,ringname,origin):

        current_app.logger.debug('#couchdb_call')
        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:

            for ring in user['rings']:
                if ring['ringname'] == ringname:

                    ring['origin'] = origin
                    self.lggr.info('Ring origin set to '+origin)

            if user.store(self.db):
                
                return True
            else:
                current_app.logger.error('Could not set origin')
                return False



    #AVISPAMODEL
    def ring_get_schema_from_view(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        
        
        current_app.logger.debug('#couchdb_call:'+db_ringname+'->ring_get_schema_from_view()')
        db = self.couch[db_ringname]

        options = {}
        result  = db.iterview('ring/schema',1,**options)

        for row in result:  
            #current_app.logger.debug('row.value.fields:')
            #current_app.logger.debug(row.value['fields'])    
            schema = {}
            #schema['rings']=row.value
            schema['fields']=row.value['fields']
            schema['rings']=row.value['rings']
            #schema['rings']=row.rings
            #schema['fields']=row.fields

        #current_app.logger.debug('schema:')
        #current_app.logger.debug(schema)

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

        #self.lggr.info('user rings:',user_doc['rings'])
        for user_ring in user_doc['rings']:
            if user_ring['ringname']==ringname:
              
                if 'deleted' in user_ring:
                    if user_ring:
                        return False

                parameters = {}
                parameters['count'] = user_ring['count']
                if 'origin' in user_ring:
                    parameters['ringorigin'] = user_ring['origin']
                else:
                    parameters['ringorigin'] = handle

                
                return parameters


        return False

  

    #AVISPAMODEL
    def get_a_b(self,handle,ringname,limit=25,lastkey=None,endkey=None,sort=None,human=False):

        
        items = []
        i = 0

        schema = self.ring_get_schema_from_view(handle,ringname) 
        OrderedFields=[]
        for field in schema['fields']:

            if human:
                OrderedFields.insert(int(field['FieldOrder']),field['FieldName'])
            else:
                OrderedFields.insert(int(field['FieldOrder']),field['FieldId'])

            

        # sort exists if it is sent in the url as ?sort=<name-of-field>_<desc|asc>
        sort_reverse=False
        if sort:
            sort_parts = sort.split('_')
            if len(sort_parts)==2:
                if sort_parts[1].lower()=='desc':
                    sort_reverse=True
                sort= sort_parts[0]
        

        result = self.select_ring_doc_view('ring/items',handle,ringname,limit=limit,lastkey=lastkey,endkey=endkey)
        #current_app.logger.debug('result:'+str(result))
    
        

        for row in result:

            i += 1
            if lastkey and i==1:
                #If lastkey was sent, ignore first item 
                #as it was the last item in the last page
                continue

            item = self.populate_item(OrderedFields,row)

            if item:
                items.append(item)
                
        if len(items)>1 and sort:
            self.sort = sort
            items = sorted(items, key=self.sort_item_list, reverse=sort_reverse)

        return items


    def select_ring_doc_view(self,dbview,handle,ringname,limit=25,key=None,batch=None,lastkey=None,endkey=None):

        # https://pythonhosted.org/CouchDB/client.html#couchdb.client.Database.iterview

        db_ringname=str(handle)+'_'+str(ringname)
        #current_app.logger.debug('#couchdb_call')
        db = self.couch[db_ringname] 
 
        if not batch : 
            batch = 500

        options = {}
        if key:
            options['key']=str(key)
        if lastkey:
            limit +=1
            options['startkey']=lastkey  #Where the last page left 

        if endkey:
            options['endkey']=endkey

        options['limit']=limit #Number of results per page  
        result = db.iterview(dbview,batch,**options)

        #options['key']='4393588627'
        
        #options['startkey_docid']='4393588627'
        #options['endkey']='4393588626'
        #options['endkey_docid']=4


        
        # result carries all the items in that page


        return result


    def populate_item(self,OrderedFields,row):
        item = collections.OrderedDict()
        if 'id' in row:        
            item[u'_id'] = row['id']

            for fieldname in OrderedFields:
                if fieldname in row['value']:
                    if row['value'][fieldname]:
                        item[fieldname] = row['value'][fieldname]

                        if fieldname+'_flag' in row['value']:
                                item[fieldname+'_flag'] = row['value'][fieldname+'_flag']
                        if fieldname+'_rich' in row['value']:
                            item[fieldname+'_rich'] = row['value'][fieldname+'_rich']


            return item
        else:
            return False
        


    def sort_item_list(self,items):
        if self.sort:
            if self.sort in items:
                return items[self.sort]
            else:
                return items[1:]
        else:
            return items[1:]


    
    
    def subtract_rich_data(self, field, external_uri_list,request_url,author):

        r_item_values = {}
        r_rich_values = {}
        r_history_values = {}


        if field['FieldId'] not in r_history_values:
            r_history_values[field['FieldId']] = []
        elif type(history_values[field['FieldId']]) is not list:
            r_history_values[field['FieldId']] = []


        #########

        self.lggr.info(field['FieldName']+'('+field['FieldId']+') is a RICH Field ')

        #1. Convert values to list
        #external_uri_list = request.form.get(field['FieldName']).split(',')
        item_value = []

        for external_uri in external_uri_list:
            
            #2. The field['FieldCardinality'] should be 'multiple' in order to accept more than one value
            # If cardinality is 'single' but still you are getting multiple entries you should only use the first one.         
            count = 0 
            if field['FieldCardinality'] == 'Single' and count>1:
                break
            count += 1


            #3. In case of valid multiple cardinality you need to enter as many items in the rich list for that field.
            self.lggr.info('external_uri '+str(external_uri))
            urlparts = urlparse.urlparse(external_uri)

            if urlparts.scheme == '' or urlparts.netloc == '':
                # You are getting ids not uris. Try to make it up with the suggested source indicated in the schema
                urlparts = urlparse.urlparse(field['FieldSource'])
                try: 
                    p = urlparts.path +'/'+str(int(external_uri))
                    p_url=urlparse.urlunparse((urlparts.scheme, urlparts.netloc, p , '', '', ''))
                    urlparts = urlparse.urlparse(p_url)
                except(ValueError):
                    # The id is a string. Maybe the field was converted from textbox to reference later on.
                    break





            #current_app.logger.debug('urlparts '+ str(urlparts))

            pathparts = urlparts.path.split('/')
            if pathparts[1]!='_api':
                if pathparts[2]=='_collections':
                    del pathparts[2] # /_collections
                    del pathparts[3] # /<collection_name>
                    sufix_corrected_path = '/'.join(pathparts)
                    corrected_path = '/_api/'+sufix_corrected_path
                    canonical_path = '/'+sufix_corrected_path
                    external_handle = pathparts[1]
                    external_ringname = pathparts[4]
                    external_idx = pathparts[5]
                else:
                    corrected_path = '/_api'+urlparts.path
                    canonical_path = urlparts.path
                    external_handle = pathparts[1]
                    external_ringname = pathparts[2]
                    external_idx = pathparts[3]
            else:
                corrected_path = urlparts.path   
                external_handle = pathparts[2]
                external_ringname = pathparts[3]
                external_idx = pathparts[4]
                canonical_path = '/'+external_handle+'/'+external_ringname+'/'+external_idx

                



            query = 'schema=1'
            url=urlparse.urlunparse((urlparts.scheme, urlparts.netloc, corrected_path , '', query, ''))
            source_url = urlparse.urlunparse((urlparts.scheme, urlparts.netloc, corrected_path , '', '', ''))
            canonical_url = urlparse.urlunparse((urlparts.scheme, urlparts.netloc, canonical_path , '', '', ''))


            external_host=urlparse.urlunparse((urlparts.scheme, urlparts.netloc, '', '', '', ''))
            self.lggr.info('external_host: '+str(external_host))

            rqurl = urlparse.urlparse(request_url)
            local_host=urlparse.urlunparse((rqurl.scheme, rqurl.netloc, '', '', '', ''))
            self.lggr.info('local_host: '+str(local_host))
        
            if local_host==external_host:
                self.lggr.info('Data source is in the same server')
                self.lggr.info('Retrieving source locally at:'+external_handle+'/'+external_ringname+'/'+external_idx)

                result_rich_item = self.get_a_b_c(None,external_handle,external_ringname,external_idx,human=True)
                if result_rich_item:
                    self.lggr.info('Retrieving data successful')
                    self.lggr.info(result_rich_item)
                    rich_item = result_rich_item
                else:
                    self.lggr.error('Could not retrieve data locally')


                rs = self.ring_get_schema_from_view(external_handle,external_ringname)

                #current_app.logger.debug('rich_rs:'+str(rs))
                #current_app.logger.debug('rich_item:'+str(rich_item))
                
                

                
            else:
                self.lggr.info('Data source is in another server')
                self.lggr.info('Retrieving source at:'+str(url))

                r = requests.get(url)

                self.lggr.info(r)

                self.lggr.info(r.text)

                #current_app.logger.debug('Raw JSON schema:'+str(r.text))
                rs = json.loads(r.text)
                #current_app.logger.debug('rich_rs:'+str(rs))
                rich_item = rs['items'][0]
                #current_app.logger.debug('rich_item:'+str(rich_item))
                

            if not rich_item:

                rich_item = {
                           '_source': url,
                           'error':404
                           }
                #It didn't find the external item
            
            rich_item_dict = {}
            #Nice to include where we got the information from
            rich_item_dict['_source'] = source_url
            # Converting the ordered_dictionary to regular dictionary
            for j in rich_item:
                rich_item_dict[j] = rich_item[j]

            item_value.append(canonical_url)
            
            if field['FieldId'] not in r_rich_values:
                r_rich_values[field['FieldId']] = []
            elif type(r_rich_values[field['FieldId']]) is not list:
                r_rich_values[field['FieldId']] = []

            r_rich_values[field['FieldId']].append(rich_item_dict)
                #rich_values[field['FieldName']] = rich_value


            history_item_dict = {}
            history_item_dict['date'] = datetime.now()
            history_item_dict['author'] = author
            history_item_dict['before'] = ''
            history_item_dict['after'] = rich_item_dict['_source']+'/'+ rich_item_dict['_id']
            history_item_dict['action'] = 'New item. RICH field'
            history_item_dict['doc'] = rich_item_dict

            r_history_values[field['FieldId']].append(history_item_dict)

        #Here you joint the values
        r_item_values[field['FieldId']] = ','.join(item_value)
        
        return (r_item_values,r_rich_values,r_history_values)




    #AVISPAMODEL
    def post_a_b(self,request,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        current_app.logger.debug('#couchdb_call')
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        
        item_values = {}
        rich_values = {}
        history_values = {}
        flag_values = {}
        fields = schema['fields']

        self.lggr.info("post_a_b raw arguments sent:"+str(request.form))
        


        for field in fields:
            
            #current_app.logger.debug(field['FieldName']+' ('+field['FieldId']+') content: '+str(request.form.get(field['FieldName'])))
            #current_app.logger.debug(field['FieldName']+' ('+field['FieldId']+') type: '+str(type(request.form.get(field['FieldName']))))

            #current_app.logger.debug('FieldSource:'+str(field['FieldSource']))
            #current_app.logger.debug('FieldWidget:'+str(field['FieldWidget']))

            

            #Detect if FieldWidget is "select" . If it is you are getting an ID. 
            #You need to query the source to get the real value and the _rich values
            if field['FieldSource'] and (field['FieldWidget']=='select' or field['FieldWidget']=='items'):
                
                #Form values could be named after FieldName or FieldId, we accept both ways. (second one is more explicit)
                external_uri_list = []

                if field['FieldName'] in request.form:
                    if len(request.form.get(field['FieldName']))!=0:
                        external_uri_list = request.form.get(field['FieldName']).split(',')                     
                elif field['FieldId'] in request.form:
                    if len(request.form.get(field['FieldId']))!=0:
                        external_uri_list = request.form.get(field['FieldId']).split(',')
                

                if len(external_uri_list) > 0:
                    r_item_values,r_rich_values,r_history_values = self.subtract_rich_data(field,external_uri_list,request.url,current_user.id)
                    item_values.update(r_item_values)
                    rich_values.update(r_rich_values)
                 
            else:

                #Not a rich widget. Will not have rich data
                self.lggr.info(field['FieldName'] +' ('+field['FieldId']+') is NOT a RICH Field ')

                #Form values could be named after FieldName or FieldId, we accept both ways. (second one is more explicit)
                if field['FieldName'] in request.form:
                    if len(request.form.get(field['FieldName']))!=0:
                        item_values[field['FieldId']] = request.form.get(field['FieldName'])
                elif field['FieldId'] in request.form:
                    if len(request.form.get(field['FieldId']))!=0:
                        item_values[field['FieldId']] = request.form.get(field['FieldId'])

                            
                #This will record the history for the first entry in the item history

            if field['FieldId'] not in history_values:
                history_values[field['FieldId']] = []
            elif type(history_values[field['FieldId']]) is not list:
                history_values[field['FieldId']] = []


            if field['FieldId'] in item_values:

                history_item_dict = {}
                history_item_dict['date'] = datetime.now()
                history_item_dict['author'] = current_user.id
                history_item_dict['before'] = ''
                history_item_dict['after'] = item_values[field['FieldId']]
                history_item_dict['action'] = 'New item'
                
                history_values[field['FieldId']].append(history_item_dict)
                    #history_values[field['FieldName']] = history_list


            #Subtract the Flag

            if 'flag_'+field['FieldName'] in request.form:
                if len(request.form.get('flag_'+field['FieldName']))!=0:
                    flag_values[field['FieldId']] = request.form.get('flag_'+field['FieldName'])
            elif 'flag_'+field['FieldId'] in request.form:
                if len(request.form.get('flag_'+field['FieldId']))!=0:
                    flag_values[field['FieldId']] = request.form.get('flag_'+field['FieldId'])



        RingClass = self.ring_create_class(schema)
        item = RingClass()        
        item._id= str(random.randrange(1000000000,9999999999))
        #item.deleted = 
        item.items.append(**item_values)
        #current_app.logger.debug("rich_values:"+str(rich_values))
        #item.rich.append(**rich_values)
        item.rich.append(**rich_values)
        item.history.append(**history_values)
        item.flags.append(**flag_values)
        
        
        if item.store(db):
        
            self.increase_item_count(handle,ringname)

            return item._id

        return False


    #AVISPAMODEL
    def get_a_b_c(self,request,handle,ringname,idx,human=False):

        schema = self.ring_get_schema_from_view(handle,ringname)   
        OrderedFields=[]
        for field in schema['fields']:
            if human:
                OrderedFields.insert(int(field['FieldOrder']),field['FieldName'])
            else:
                OrderedFields.insert(int(field['FieldOrder']),field['FieldId'])


        current_app.logger.debug('select_ring_doc_view(ring/items,'+str(handle)+','+str(ringname)+','+str(idx)+') ')            
        
        result = self.select_ring_doc_view('ring/items',handle,ringname,key=idx)
        
        current_app.logger.debug('result:'+str(result))
        
        for row in result:

            #current_app.logger.debug('row:'+str(row))

            item = self.populate_item(OrderedFields,row)

            if item:
                return item

        #There is no item. It could have been deleted.
        return False


    #AVISPAMODEL
    def put_a_b_c(self,request,handle,ringname,idx):

        self.lggr.info('put_a_b_c()')

        db_ringname=str(handle)+'_'+str(ringname)
        #current_app.logger.debug('#couchdb_call')
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)

        needs_store = False
        
        item_values = {}
        history_values = {}
        rich_values = {}
        fields = schema['fields']

        if request.form.get('_public'):
            item['public']=True
        else:
            item['public']=False



        for field in fields:
            
            #VALUES
            new = ''
            old = ''

            if item.items[0][field['FieldId']] == None:
                old = item.items[0][field['FieldId']]
            else:
                old = unicode(item.items[0][field['FieldId']])

            
            if field['FieldName'] in request.form:
                if len(request.form.get(field['FieldName']))!=0:
                    new = unicode(request.form.get(field['FieldName']))
            elif field['FieldId'] in request.form:
                if len(request.form.get(field['FieldId']))!=0:
                    new = unicode(request.form.get(field['FieldId']))

            #old = old.strip()
            new = new.strip()

            if new == '':
               new = None

            if old == new:
                self.lggr.info(field['FieldId']+' did NOT change')
                pass
                #self.lggr.info(field['FieldName']+' ('+field['FieldId']+') did not change')  

            else:
                
                needs_store = True
                self.lggr.info(field['FieldName']+' ('+field['FieldId']+') changed. Old: "'+ str(old) +'" ('+ str(type(old)) +')'+\
                                '  New: "'+ str(new) + '" ('+ str(type(new)) +')' )

                                    #This will record the history for the item update 
                history_item_dict = {}
                history_item_dict['date'] = str(datetime.now())
                history_item_dict['author'] = current_user.id
                history_item_dict['before'] = str(old) +' '+ str(type(old)) 
                history_item_dict['after'] = str(new) + ' '+ str(type(new))
                history_item_dict['action'] = 'Update item'

                item.history[0][field['FieldId']].append(history_item_dict)


                item.items[0][field['FieldId']] = new

            
            #FLAGS

            #Lets check if there is a flag object in the document
            if type(item.flags) is list:
                item.flags = []
                item.flags.append({})


            if field['FieldId'] not in item.flags[0]:
                item.flags[0][field['FieldId']] = ''

            old_flag = unicode(item.flags[0][field['FieldId']])

            if 'flag_'+field['FieldName'] in request.form:
                if len(request.form.get('flag_'+field['FieldName']))!=0:
                    new_flag = unicode(request.form.get('flag_'+field['FieldName']))
            elif 'flag_'+field['FieldId'] in request.form:
                if len(request.form.get('flag_'+field['FieldId']))!=0:
                    new_flag = unicode(request.form.get('flag_'+field['FieldId']))

            if old_flag == new_flag:
                self.lggr.info('Flag for: '+field['FieldName']+' ('+field['FieldId']+') did not change') 

            else:
                needs_store = True

                self.lggr.info(field['FieldName']+'_flag ('+field['FieldId']+') changed. Old: "'+ str(old_flag) +'" ('+ str(type(old_flag)) +')'+\
                                '  New: "'+ str(new_flag) + '" ('+ str(type(new_flag)) +')' )

                history_item_dict = {}
                history_item_dict['date'] = str(datetime.now())
                history_item_dict['author'] = current_user.id
                history_item_dict['before'] = str(old_flag) +' '+ str(type(old_flag)) 
                history_item_dict['after'] = str(new_flag) + ' '+ str(type(new_flag))
                history_item_dict['action'] = 'Update flag'

                item.history[0][field['FieldId']].append(history_item_dict)

                item.flags[0][field['FieldId']] = new_flag

            # END FLAGS


                
            if field['FieldSource'] and (field['FieldWidget']=='select' or field['FieldWidget']=='items'):
            
                needs_store = True
                external_uri_list = []

                #Form values could be named after FieldName or FieldId, we accept both ways. (second one is more explicit)
                if field['FieldName'] in request.form:
                    if len(request.form.get(field['FieldName']))!=0:
                        external_uri_list = request.form.get(field['FieldName']).split(',')                     
                elif field['FieldId'] in request.form:
                    if len(request.form.get(field['FieldId']))!=0:
                        external_uri_list = request.form.get(field['FieldId']).split(',')
                
                if len(external_uri_list) > 0:
                    r_item_values,r_rich_values,r_history_values = self.subtract_rich_data(
                                                                        field,
                                                                        external_uri_list,
                                                                        request.url,
                                                                        current_user.id)
                    item_values.update(r_item_values)
                    rich_values.update(r_rich_values)


                    #Repair rich object if needed
                    if 'rich' not in item:
                        current_app.logger.debug('REPAIR FLAG 1')
                        #item.rich = []
                        #rich_dict = {}
                        #item.rich.append(rich_dict)
                    elif type(item.rich) is not list:
                        current_app.logger.debug('REPAIR FLAG 2')
                        #item.rich = []
                        #rich_dict = {}
                        #item.rich.append(rich_dict)
                    elif type(item.rich[0]) is not dict:
                        current_app.logger.debug('REPAIR FLAG 3')
                        #rich_dict = {}
                        #item.rich.append(rich_dict)

                  
                    #1. Save in memory what is in rich data just in case we got a 404
                    old_rich = item.rich[0][field['FieldId']]
                    old_rich_dictionary = {}
                    for old_r in old_rich:
                        if '_source' in old_r:
                            old_rich_dictionary[old_r['_source']] = old_r

                    #current_app.logger.debug('old_rich:'+str(old_rich))
                    #current_app.logger.debug('old_rich_dictionary:'+str(old_rich_dictionary))

                    #2. Check if we got a 404
                    if field['FieldId'] in r_rich_values:
                        for new_rich_value in r_rich_values[field['FieldId']]:
                            if 'error' in new_rich_value:
                                #3. Check if we can at least have old version (better than nothing)
                                if new_rich_value['_source'] in old_rich_dictionary: 
                                    new_rich_value = old_rich_dictionary[new_rich_value['_source']]

                    if r_rich_values:
                                    
                        item.rich[0][field['FieldId']] = r_rich_values[field['FieldId']]

        if needs_store:
            if item.store(db):      
                return item._id
        else:
            return item._id

        return False


    def delete_a_b_c(self,request,handle,ringname,idx):


        db_ringname=str(handle)+'_'+str(ringname)
        #current_app.logger.debug('#couchdb_call')
        db = self.couch[db_ringname]

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)

        fields = schema['fields']
        for field in fields:
        
            old = unicode(item.items[0][field['FieldId']])

            history_item_dict = {}
            history_item_dict['date'] = str(datetime.now())
            history_item_dict['author'] = current_user.id
            history_item_dict['before'] = str(old) +' '+ str(type(old)) 
            history_item_dict['after'] = ''
            history_item_dict['action'] = 'Delete item'
            item.history[0][field['FieldId']].append(history_item_dict)

        item.deleted = True

        if item.store(db): 

            self.decrease_item_count(handle,ringname)

            return item._id

        return False




    