# RingsModel.py
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

from flask import flash
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField, Mapping 
from couchdb.design import ViewDefinition
from couchdb.http import ResourceNotFound
from RingsSchema import RingsSchema
#from ElasticSearchModel import ElasticSearchModel
from AvispaLogging import AvispaLoggerAdapter

from MyRingUser import MyRingUser
from MainModel import MainModel
from env_config import TEMP_ACCESS_TOKEN

from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)


class RingsModel:

    def __init__(self,tid=False,ip=False):

        logger = logging.getLogger('Avispa')
        self.lggr = AvispaLoggerAdapter(logger, {'tid': tid,'ip': ip})
        
        self.MAM = MainModel(tid=tid,ip=ip)

    #DEPRECATED
    def ring_data_from_user_doc(self,handle,ringd): 
        '''
        Subtracts relevant ring data from user doc

        @UNITTEST: True

        @MONGODB
          -This function is being deprecated by MongoDB refactoring
          -Refer to user_get_rings_mongodb()

        @IN:
          handle = (string)

          ringd =
          {
            "ringname":(string),
            "version":(string),
            "origin":(string),
            "count":(string)
          }


        @OUT:
          {
            "ringname":(string),
            "ringversion":(string),
            "ringorigin":(string),
            "ringversionh":(string),
            "count":(string)
          }
        '''  


        r = {}

        r['ringname'] = str(ringd['ringname'])
        r['ringversion'] = str(ringd['version'])

        if 'origin' in ringd:
            r['ringorigin'] = str(ringd['origin'])
        else:
            r['ringorigin'] = str(handle)

        r['ringversionh'] = str(ringd['version']).replace('-','.')
        r['count'] = ringd['count']

        return r

    #DEPRECATED
    def ring_data_from_schema(self,schema):
        '''
        Subtracts relevant ring data from schema

        @UNITTEST: True

        @MONGODB
          -This function is being deprecated by MongoDB refactoring
          -Refer to user_get_rings_mongodb()

        @IN:
          schema = 
          {
            "rings":[
              {
                 "RingDescription":(string),
                 "RingLabel":(string),
                 ...
              }
            ],
            "fields":[]
          }

        @OUT:
          {
            "ringdescription":(string),
            "ringlabel":(string),
            "fields":[],
            "rings":[]
          }
        '''

        r = {}

        if 'RingDescription' in schema['rings'][0]:
            r['ringdescription'] = schema['rings'][0]['RingDescription'] 
        else:
            r['ringdescription'] = False
  
        if 'RingLabel' in schema['rings'][0]:               
            r['ringlabel'] = schema['rings'][0]['RingLabel'] 
        else:
            r['ringlabel'] = False 

        r['fields'] = schema['fields']
        r['rings'] = schema['rings']

        return r


    #DEPRECATED
    def subtract_ring_data(self,handle,ringlist):
        ''' 
        Joins data coming from the user doc and the schemas

        @MONGODB
          -This function is being deprecated by MongoDB refactoring
          -Refer to user_get_rings_mongodb()

        @IN:
          handle = (string)
          ringlist = 
          [
            {
              "ringname":(string),
              "version":(string),
              "origin":(string),
              "count":(string)
            },
          ]

        @OUT:
          [{
            "ringname":(string),
            "ringversion":(string),
            "ringorigin":(string),
            "ringversionh":(string),
            "count":(string),
            "ringdescription":(string),
            "ringlabel":(string),
            "fields":[],
            "rings":[]
          },{}]

        @MONGODB
          -This function is being deprecated by MongoDB refactoring
 

        '''

        
        data = []

        for ringobj in ringlist:
            schema = self.ring_get_schema_from_view(handle,str(ringobj['ringname'])) # ACTIVE COLLABORATION
           
            if schema and 'deleted' not in ringobj:
                r1 = self.ring_data_from_user_doc(handle,ringobj) # ACTIVE COLLABORATION
                r2 = self.ring_data_from_schema(schema) # ACTIVE COLLABORATION
                r = dict(r1,**r2)
                data.append(r)

        return data


    #REFACTOR REPLACED
    def user_get_rings(self,handle):
        '''
        Output ring data given a handle

        @REPLACEDBY:
          user_get_rings_mongodb()

        @NOTES:
          -Refactoring this function around MongoDB aggregation will eliminate the need of all
           downstream functions


        @IN: 
          handle = (string)

        @OUT:
          {
            "ringname":(string),
            "ringversion":(string),
            "ringorigin":(string),
            "ringversionh":(string),
            "count":(string),
            "ringdescription":(string),
            "ringlabel":(string),
            "fields":[],
            "rings":[]
          }

        @EXCEPTION:
          -No rings for this user

        @MONGODB
          -This function is being deprecated by MongoDB refactoring

        '''

  
        try:
            self.lggr.info('flag1:'+handle)
            doc = self.MAM.select_user(handle) # ACTIVE COLLABORATION 
            self.lggr.info('flag2')
            self.lggr.info(doc)
            data = self.subtract_ring_data(handle,doc['rings']) # ACTIVE COLLABORATION
            self.lggr.info('flag3')
            self.lggr.info(data)

        except (ResourceNotFound, TypeError) as e:

            #BUG: This exception gets triggered even if the ring does exist
            #The problem has to do with pagination. It can't find it in the current page

            #flash("You have no rings yet, create one!")
            self.lggr.error("Notice: Expected error:%s,%s"%(sys.exc_info()[0] , sys.exc_info()[1]))
            #self.lggr.debug('Notice: No rings for this user.')
            data = []

        return data


    #REFACTORED
    def user_get_rings_mongodb(self,handle):
        '''
        @MONGODB:
          - "ringversion" requires string substitution which the aggregation framework doesn't offer
          - "rings" is a field that needs to be removed as same information is already available

          db._ring.aggregate([
            {
              $lookup:
                {
                  from: "_field",
                  localField: "_id",
                  foreignField: "parent",
                  as: "_field"
                },
              $project:
                {
                  "ringname":"$ringname",
                  "ringversion":"$ringversion",
                  "ringorigin":"$ringorigin",
                  "ringversionh":"$ringversion",
                  "count":"$count",
                  "ringdescription":"$ringdescription",
                  "ringlabel":"$ringlabel,
                  "fields":"$_field",
                  "rings": []
                }
            } 
          ])
        '''
        from pymongo import MongoClient
        from bson.son import SON

        db = MongoClient().openringdb

        # Aggregates rings for one user

        handle_ring_agg = [
            {"$match":{
                "handle":handle
            }},
            {"$lookup":{
                "from": "_ring",
                "localField": "_id",
                "foreignField": "_handle",
                "as": "_ring"
            }},
            {"$project":{
                "ringname":"$ringname"
            }}
        ]

        ringlist = list(db._ring.aggregate(handle_ring_agg))

        data = []
        for k,v in ringlist:

            # Aggregates fields for one ring
            ring_field_agg = [
                {"$match":{
                    "ringname":v
                }},
                {"$lookup": {
                    "from": "_field",
                    "localField": "_id",
                    "foreignField": "_ring",
                    "as": "_field"
                }},
                {"$project": {
                    "ringname":"$ringname",
                    "ringversion":"$ringversion",
                    "ringorigin":"$ringorigin",
                    "ringversionh":"$ringversion",
                    "count":"$count",
                    "ringdescription":"$ringdescription",
                    "ringlabel":"$ringlabel",
                    "fields":"$_field",
                    "rings": []
                }}
            ]

            r = list(db._ring.aggregate(ring_field_agg))


            data.append(r)

        return data

    
    def ring_set_db(self,handle,ringname,ringversion):
        '''
        Creates new ring DB, its views and add it to the userdoc

        @IN:
          handle = (string)
          ringname = (string)
          ringversion = (string)

        @OUT:
          (boolean)

        @EXCEPTION:
          - Can't create DB

        @COLLATERAL:
          - Creates DB
          - Creates DB Views
          - Adds ring to userdoc

        '''

           
        #db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db_ringname=str(handle)+'_'+str(ringname)
        db_ringname = db_ringname.replace(" ","")

        try:            
            
            self.MAM.create_db(db_ringname)
            self.ring_set_db_views(db_ringname) #Sets all the DB Views needed for this new ring
            self.user_add_ring(handle,ringname,ringversion) #Adds the ring to the user's list
            return True    

        except:
            self.lggr.error ("Unexpected error:"+str( sys.exc_info()[0] )+str( sys.exc_info()[1]))
            #flash(u'Unexpected error:'+ str(sys.exc_info()[0]) + str(sys.exc_info()[1]),'error')
            self.rs_status='500'
            raise
            return False


    
    def ring_set_db_views(self,db_ringname,specific=False):
        '''
        Creates DB Views

        @IN
          db_ringname = (string)
          specific = (string)

        @OUT
          True (fixed)

        @COLLATERAL
          -Creates DB Views
        '''

        db = self.MAM.select_db(db_ringname)
   
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
                            var c = {}; 

                            for (var key in doc.history[0]) {           
                               for (var h in doc.history[0][key]){ 
                                   var author = doc.history[0][key][h]['author'];
                                   var action = doc.history[0][key][h]['action'];
                                   var date = doc.history[0][key][h]['date'].substring(0,16);
                                   var before = doc.history[0][key][h]['before'];
                                   var after = doc.history[0][key][h]['after'];

                                   if(!(author in c)){               
                                       var a = {};
                                       a['new'] = {};
                                       a['update'] = {};                
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
                            for(var ax in c){
                                emit(ax, c[ax]); 
                            }       
                         }
                      }
                    }

                   ''')

            view.get_doc(db)
            view.sync(db)

        return True


    def user_add_ring(self,handle,ringname,ringversion):
        '''
        Adds ring to userdoc

        @IN: 
          handle = (string)
          ringname = (string)
          ringversion = (string)

        @OUT:
          True (fixed)

        @COLLATERAL
          -Adds ring to userdoc
        '''

        self.lggr.info("handle:",handle)

        doc = self.MAM.select_user(handle)

        doc.rings.append(ringname=str(ringname),version=str(ringversion),added=datetime.now(),count=0)

        self.MAM.post_user_doc(doc)

        return True


    def user_delete_ring(self,handle,ringname):
        '''
        Deletes ring and its references (no tombstones)
        It won't delete ringdb if it is not in the userdoc

        @IN:
          handle = (string)
          ringname = (string)

        @OUT:
          (boolean)

        @EXCEPTION:
          -Ring doesn't exist in userdoc
          -Ring doesn't exist in DB

        @COLLATERAL
          - Delete ring from userdoc
          - Delete ring DB
          - Delete ring from collections
        '''

        doc = self.MAM.select_user(handle)
        
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
                #self.lggr.debug()
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
                
        if self.MAM.post_user_doc(doc):
            return True

        
        return False


    def user_hard_delete_ring(self,handle,ringname,ringversion):
        '''
        Delete ring from DB 

        @NOTES
          - user_delete_ring() does the same but it deletes first the db 
            and then cleanses the userdoc

        @IN:
          handle = (string)
          ringname = (string)
          ringversion = (string)

        @OUT:
          (boolean)

        @COLLATERAL:
          - Delete ring DB
          - Delete ring from userdoc
          


        '''

        #dbname = handle+'_'+ringname+'_'+ringversion
        dbname = handle+'_'+ringname
        if self.MAM.delete_db(dbname):
            self.lggr.info('Deleted from DB')
            del1 = True

        doc = self.MAM.select_user(handle)
        rings = doc['rings']
        count = 0
        for ring in rings:
            if ring['ringname']==ringname and ring['version']==ringversion:
                #Here you should also make a hard delete not only a tombstone
                del doc['rings'][count]

            count += 1

                #ring['deleted']=True
                
        if self.MAM.post_user_doc(doc):
            self.lggr.info('Deleted from USERDB')
            del2 = True
      

        if del1 and del2:
            return True
        else:
            return False


    def ring_get_schema(self,handle,ringname):
        '''
        Returns ring schema

        @NOTES:
          -Considering deprecating this function for ring_get_schema_from_view

        @IN:
          handle = (string)
          ringname = (string)

        @OUT:
          {(ring schema)}

        
        '''

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.MAM.select_db(db_ringname)
        schema = RingsSchema.load(db,'schema')

        return schema


    #DEPRECATED
    def ring_get_item_document(self,handle,ringname,idx):
        ''' 
        Retrieve one ring document from its db

        @DEPRECATED
         -Nobody is using it but old patches

        @NOTES:
         - Is any function currently using this? 
         - 3 calls to the DB to subtract one document?

        @IN:
          handle:(string)
          ringname:(string)
          idx:(string)

        @OUT:
          {(ring_item)}


        '''

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.MAM.select_db(db_ringname)
        item = RingClass.load(db,idx)

        return item


    
    def ring_set_schema(self,handle,ringname,ringversion,pinput,ringprotocol,fieldprotocol):
        '''
        Creates Ring Schema doc if it doesn't exist. Updates current one if it does

        @IN:
          handle = (string)
          ringname = (string)
          ringversion = (string)
          pinput = {}
          ringprotocol = []
          fieldprotocol = []

        @OUT:
          "ok" (fixed)

        @COLLATERAL
          - create/update schema doc
        '''

        if ringversion == 'None' or ringversion == None:
            ringversion = ''

        #db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        db_ringname=str(handle)+'_'+str(ringname)
        db = self.MAM.select_db(db_ringname)
        numfields = len(pinput['fields'])
        schema = RingsSchema.load(db,'schema')

        # Creates Ring Schema if it doesn't exist. Uses current one if it exists.
        if schema:
            action = 'edit'
        else:       
            schema = RingsSchema()
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


            #self.lggr.debug('args_f:')
            #self.lggr.debug(args_f)

            if action == 'new':
                args_f['FieldId'] = self.MAM.random_hash_generator(36)

                schema.fields.append(**args_f)
                
            elif action == 'edit' :

                if 'FieldId' not in schema.fields[i]:
                    args_f['FieldId'] = self.MAM.random_hash_generator(36)

                for y in args_f:
                    schema.fields[i][y] = args_f[y]

            args_f={}

        #self.lggr.debug(schema)

        
        schema.store(db)

        return 'ok'

    
    # DEPRECATED
    def _schema_create_class(self,numfields,ringprotocol,fieldprotocol):
        '''
        Create schema class
        
        @NOTES: 
          -This function is deprecated. Now we just instantiate RingsSchema class

        @IN:
          numfields = (integer)
          ringprotocol = []
          fieldprotocol = []

        @OUT:
          (schema_class)
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


    def ring_class_field_type(self,fieldtype):
        '''
        Maps ring datatype with db type

        @NOTES:
          -Needed to create couchdb specific mapping.
          
        @IN:
          fieldtype = (string)

        @OUT:
          (function)

        '''

        #Types : TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField
        if fieldtype == 'INTEGER':
            return IntegerField()
        elif fieldtype == 'OBJECT':
            return DictField()
        elif fieldtype == 'ARRAY':
            return ListField()
        elif fieldtype == 'BOOLEAN':
            return BooleanField()
        else:
            return TextField()

    def ring_class_field_history(self):
        '''
        Creates object that contains field history

        @OUT:
          (Object)

        '''

        d = {}
        d['date']=DateTimeField()
        d['author']=TextField()
        d['before']=TextField()
        d['after']=TextField()
        d['action']=TextField()
        d['doc']=DictField()
        return ListField(DictField(Mapping.build(**d)))

    def ring_class_prepare_class_arguments(self,schema):
        '''
        Prepares argument objects for Ring Class 

        @IN:
          schema = (ring_schema)

        @OUT:

          {
            'type':{(fieldid):(object)},
            'rich':{(fieldid):(object)},
            'history':{(fieldid):(object)},
            'meta':{(fieldid):(object)},
            'flags':{(fieldid):(object)}
          }

        '''

        args = {'type':{},'rich':{},'history':{},'meta':{},'flags':{}}

        for field in schema['fields']:
            args['type'][field['FieldId']] = self.ring_class_field_type(field['FieldType'])
            args['rich'][field['FieldId']] = ListField(DictField())
            args['history'][field['FieldId']] = self.ring_class_field_history()
            args['meta'][field['FieldId']] = DictField()
            args['flags'][field['FieldId']] = TextField()

        return args

   
    def ring_create_class(self,schema):
        '''
        Creates the Ring Class 

        @NOTES:
          - This class maps the item document that contains the data (not the schema).

        @INPUT:
          schema = (object)

        @OUTPUT:
          (class)
           
        '''

        args = self.ring_class_prepare_class_arguments(schema)

        RingClass = type('RingClass',
                         (Document,),
                         {
                            '_id' : TextField(),
                            'added' : DateTimeField(default=datetime.now()),
                            'license' : TextField(),
                            'public' : BooleanField(default=False),
                            'deleted' : BooleanField(default=False),
                            'items': ListField(DictField(Mapping.build(
                                                    **args['type']
                                                ))),
                            'rich': ListField(DictField(Mapping.build(
                                                    **args['rich']
                                                ))),
                            'history': ListField(DictField(Mapping.build(
                                                    **args['history']
                                                ))),
                            'flags': ListField(DictField(Mapping.build(
                                                    **args['flags']
                                                ))),
                            'meta': ListField(DictField(Mapping.build(
                                                    **args['meta']
                                                )))
                                               }) 

        return RingClass

    
    def get_item_count(self,handle,ringname):
        '''
        Ring item count from the userdoc

        @IN: 
          handle = (string)
          ringname = (string)

        @OUT:
          ok:(integer)
          ko: False
        '''

        doc = self.MAM.select_user(handle)
        self.lggr.info('user rings:'+str(doc['rings']))
        for user_ring in doc['rings']:
            if user_ring['ringname']==ringname:
                return user_ring['count']

        return False

    
    def put_labels(self,handle,ringname,labels):
        '''
        Writes labels into the userdoc

        @NOTES:
          - This function is in development.
          -"labels" is a list of dictionaries 

        @IN:
          handle = (string)
          ringname = (string)
          labels = [{}]

        @OUT:
          ok:True
          ko:False

        @COLLATERAL:
          - Write labels to userdoc
        '''

        # 

        labels = [{'name':'urgent', 'color':'#f00'},
         {'name':'ok', 'color':'#00f'},
         {'name':'ready', 'color':'#0f0'}]
       
        doc = self.MAM.select_user(handle)

        if doc:

            for ring in doc['rings']:
                if ring['ringname'] == ringname:
                    ring['labels'] = json.dumps(labels)
                    self.lggr.info('Labels added to the ring')

            if self.MAM.post_user_doc(doc):
                
                return True
            else:
                self.lggr.error('Could not add the labels')
                return False


    
    def increase_item_count(self,handle,ringname):
        '''
        Increase ring item count in userdoc

        @IN:
          handle = (string)
          ringname = (string)

        @OUT:
          ok:True
          ko:False

        @COLLATERAL
          -Write new count to userdoc

        '''

        doc = self.MAM.select_user(handle)

        if doc:

            for ring in doc['rings']:
                if ring['ringname'] == ringname:
                    ring['count'] += 1
                    

            if self.MAM.post_user_doc(doc):
                self.lggr.info('Item Count increased')
                return True
            else:
                self.lggr.error('Could not increase item count')
                return False

        #AVISPAMODEL
    def decrease_item_count(self,handle,ringname):
        '''
        Decrease ring item count in userdoc

        @IN:
          handle = (string)
          ringname = (string)

        @OUT:
          ok:True
          ko:False

        @COLLATERAL
          -Write new count to userdoc
          
        '''

        doc = self.MAM.select_user(handle)

        if doc:
            for ring in doc['rings']:
                if ring['ringname'] == ringname:
                    ring['count'] -= 1
                    self.lggr.info('Item Count decreased')

            if self.MAM.post_user_doc(doc):       
                return True
            else:
                self.lggr.error('Could not decrease item count')
                return False

    def set_ring_origin(self,handle,ringname,origin):
        '''
        Set ring origin parameter in userdoc

        @NOTES:
          - Same as: UPDATE origin=<origin> in USERDOC where handle=<handle> and ring=<ring> 

        @IN: 
          handle = (string)
          ringname = (string)
          origin = (string)

        @OUT:
          ok:True
          ko:False

        @COLLATERAL
          -Write origin parameter to userdoc ring
        '''

        doc = self.MAM.select_user(handle)

        if user:

            for ring in doc['rings']:
                if ring['ringname'] == ringname:

                    ring['origin'] = origin
                    self.lggr.info('Ring origin set to '+origin)

            if self.MAM.post_user_doc(doc):
                
                return True
            else:
                
                self.lggr.error('Could not set origin')
                return False


    def ring_get_schema_from_view(self,handle,ringname):
        '''
        Get ring schema from the schemas db view

        @NOTES:
          - Same footprint as ring_get_schema() but faster as this involves only one call
          - The schema is retrieved directly from a dedicated view not from the ring db

        @IN:
          handle = (string)
          ringname = (string)

        @OUT:
          {(ring_schema)}
        '''
        self.lggr.debug('Trying to get:'+handle+'/'+ringname)

        db_ringname=str(handle)+'_'+str(ringname) 
        db = self.MAM.select_db(db_ringname)       
       
        options = {}
        self.lggr.debug('++@ db.iterview(ring/schema)')
        result  = db.iterview('ring/schema',1,**options)
        self.lggr.debug('--@ db.iterview(ring/schema)')

        schema = {}

        for row in result:  
 
            schema = {}
            schema['fields']=row.value['fields']
            schema['rings']=row.value['rings']

            schema = self.schema_health_check(schema)
            
        return schema

    
    def schema_health_check(self,schema):     
        '''
        Checks that the schema has all required parameters

        @IN:
          schema = {(ring_schema)}

        @OUT:
          {(ring_schema)}
        '''

        # 1. Check if the FieldOrders are unique. If they aren't reassign
        l = len(schema['fields'])
        orderd= []
        needsrepair = False

        # Checking
        for f in schema['fields']:
            
            if f['FieldOrder']:
                if f['FieldOrder'] in orderd:
                    # Duplicated!
                    needsrepair = True
                else:
                    orderd.append(f['FieldOrder'])
            else:
                needsrepair = True

        # Repairing
        if needsrepair:
            self.lggr.info('Repairing FieldOrder. There where some duplicates')

            i = 1
            for f in schema['fields']:
                f['FieldOrder'] = i
                i = i+1
        else:
            pass
            #self.lggr.info('No need for repair')

        return schema
            


    def couchdb_pager(db, view_name='_all_docs',
                  startkey=None, startkey_docid=None,
                  endkey=None, endkey_docid=None, bulk=5000):

        '''
        Returns a page of documents

        @NOTES:
          -This function is a generator

        @DEPRECATED:
          -Not used anywhere

        @IN:
          db = (db reference)
          view_name = (string)
          startkey = (string)
          startkey_docid = (string)
          endkey = (string)
          endkey_docid = (string)
          bulk = (integer)

        @OUT:
          yields a page or results


        @USAGE: 
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


    

    def get_a_b_parameters(self,handle,ringname):
        '''
        Get the count and source from one ring

        @NOTES:
        - Similar to SELECT * from USERDOC where ringname=ringname and deleted!=True

        @IN: 
          handle = (string)
          ringname = (string)

        @OUT:
          ok:{
            "count":(string),
            "ringorigin":(string)
          }
          ko:False

        '''

        doc = self.MAM.select_user(handle) #ACTIVE COLLABORATION
        ringlist = doc['rings']

        for ringobj in ringlist:

            if ringobj['ringname']==ringname:            
                if 'deleted' in ringobj:
                    if ringobj:    
                        return False

                r = {}
                r['count'] = ringobj['count']
                if 'origin' in ringobj:
                    r['ringorigin'] = ringobj['origin']
                else:
                    r['ringorigin'] = handle
                return r

        return False

    def get_a_b_search(handle,ring,limit=None,querystring=None):
        
        pass

    
    def get_a_b(self,handle,ringname,limit=25,lastkey=None,endkey=None,sort=None,human=False):
        '''
        Get page of items

        @NOTES:
          - The "human" parameter determines whether ids or labels are returned as keys

        @IN:
          handle = (string)
          ringname = (string)
          limit = (integer)
          lastkey = (string)
          endkey = (string)
          sort = (string)
          human = (boolean)

        @OUT:
          [{(item)}]


        '''
       
        items = []
        i = 0

        schema = self.ring_get_schema_from_view(handle,ringname) 
        OrderedFields=[]
        
        for field in schema['fields']:
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
        #self.lggr.debug('result:'+str(result))

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
        '''
        Generic function to retrieve documents from any view

        @NOTES:
          -There is a function with same name in MainModel.py 
          -Both of them are used.
          -https://pythonhosted.org/CouchDB/client.html#couchdb.client.Database.iterview

        @IN:
          dbview = (string)
          handle = (string)
          ringname = (string)
          limit = (integer)
          key = (string)
          batch = (integer)
          lastkey = (string)
          endkey = (string)

        @OUT:
          [{(item)}]

        '''
        

        db_ringname=str(handle)+'_'+str(ringname)
        #self.lggr.debug('#couchdb_call')
        
        db = self.MAM.select_db(db_ringname)
 
        if not batch : 
            batch = 500

        options = {}
        if limit != '_all':
            options['limit']= int(limit) #Number of results per page 
            
        if key:
            options['key']=str(key)
        if lastkey:
            
            options['startkey']=lastkey  #Where the last page left 

        if endkey:
            options['endkey']=endkey

         
        result = db.iterview(dbview,batch,**options)

        #options['key']='4393588627'
        
        #options['startkey_docid']='4393588627'
        #options['endkey']='4393588626'
        #options['endkey_docid']=4   
        # result carries all the items in that page

        return result


    def populate_item(self,OrderedFields,preitem):
        '''
        Cleans, orders and complements every item before the output

        @NOTES:
          - Items are not output in the API as they are stored in the DB. 
          - Every item that goes out passes through this function

        @IN:
          OrderedFields = []
          preitem = {
                      "id":(string)
                      "value":{
                        "<fieldid_1>":(string),
                        "<fieldid_1>_flag":(string),
                        "<fieldid_1>_rich":(string),
                        ...
                        "<fieldid_n>":(string),
                        "<fieldid_n>_flag":(string),
                        "<fieldid_n>_rich":(string),
                      },
                    }
          }


        @OUT:
          {
            "_id" : (string),
            "<fieldid_1>":(string),
            "<fieldid_1>_flag":(string),
            "<fieldid_1>_rich":(string),
            ...
            "<fieldid_n>":(string),
            "<fieldid_n>_flag":(string),
            "<fieldid_n>_rich":(string)
          }


        '''
        item = collections.OrderedDict()

        if 'id' in preitem:        
            item[u'_id'] = preitem['id']

            for fieldid in OrderedFields:
                if fieldid in preitem['value']: 

                    self.lggr.debug(fieldid+' has type:'+str(type(preitem['value'])))

                    #Add Value
                    item[fieldid] = preitem['value'][fieldid]
                    #Add Flag
                    if fieldid+'_flag' in preitem['value']:
                        item[fieldid+'_flag'] = preitem['value'][fieldid+'_flag']
                    #Add Rich
                    if fieldid+'_rich' in preitem['value']:
                        item[fieldid+'_rich'] = preitem['value'][fieldid+'_rich']


            return item
        else:
            return False
        


    def sort_item_list(self,items):
        '''
        Sorts an item list respect a certain parameter

        @NOTES:
          -This function is coupled to get_a_b #REFACTOR

        @IN
          items = {}
          self.sort = (string)

        @OUT
          [(items)]

        '''

        if self.sort:
            if self.sort in items:
                return items[self.sort]
            else:
                return items[1:]
        else:
            return items[1:]

    
    def subtract_rich_data(self, field, external_uri_list,request_url,author):
        '''
        Expand references for one particular field and writes changes in history

        @NOTES:
          -The "field" objects comes directly from the schema
          -The "external_uri_list" string is a comma separated string of URLs. 
          -They are URIs that refer to one or multiple items from other rings (i.e: Multiple countries)
          -The "request_url" string is the url from where the request was made.
          -If the "request_url" matches with one of the referred URIs it is queried internally (hack for speed)
          -"author" is for history to have a reference on who triggered the subtraction (happens during put or post)
          -This function needs to be split in small pieces #REFACTOR

        @IN:
          field = {
            'FieldId':(string),
            'FieldName':(string),
            'FieldCardinality':(string),
            'FieldSource':(string),
            'author':(string)
          }
          external_uri_list = [(string)]
          request_url = (string)
          author = (string)

        @OUT:
          ({(r_item_values)},{(r_rich_values)},{(r_history_values)})

        '''

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


            #self.lggr.debug('urlparts '+ str(urlparts))

            pathparts = urlparts.path.split('/')
            # Pathpart is a url entered during capture
            if pathparts[1]!='_api':
                # References MUST have an _api prefix . Repair if it doesn't  
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

                



            query = 'schema=1'+'&access_token=%s'%TEMP_ACCESS_TOKEN
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

                #self.lggr.debug('rich_rs:'+str(rs))
                #self.lggr.debug('rich_item:'+str(rich_item))
                
                

                
            else:
                self.lggr.info('Data source is in another server')
                self.lggr.info('Retrieving source at:'+str(url))

                r = requests.get(url)

                self.lggr.info(r)

                self.lggr.info(r.text)

                #self.lggr.debug('Raw JSON schema:'+str(r.text))
                rs = json.loads(r.text)
                #self.lggr.debug('rich_rs:'+str(rs))
                rich_item = rs['items'][0]
                #self.lggr.debug('rich_item:'+str(rich_item))
                

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
    def post_a_b(self,rqurl,rqform,handle,ringname):
        '''
        Creates a new item in the ring

        @NOTES:
          - "rqurl" are the arguments that come via url
          - "rqform" are the arguments that come via form


        @IN:
          rqurl = {(string):(string),}
          rqform = {(string):(string),}
          handle = (string)
          ringname = (string)

        @OUT:
          ok:(item_id)
          ko:False

        @COLLATERAL:
          - Create new document in DB
          - Increase item count in userdoc

        '''

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.MAM.select_db(db_ringname)

        schema = self.ring_get_schema(handle,ringname)
        
        item_values = {}
        rich_values = {}
        history_values = {}
        flag_values = {}
        fields = schema['fields']

        self.lggr.info("post_a_b raw arguments sent:"+str(rqform))

        for field in fields:
       
            #Detect if FieldWidget is "select" . If it is you are getting an ID. 
            #You need to query the source to get the real value and the _rich values
            if field['FieldSource'] and (field['FieldWidget']=='select' or field['FieldWidget']=='items'):
                
                #Form values could be named after FieldName or FieldId, we accept both ways. (second one is more explicit)
                external_uri_list = []

                if field['FieldName'] in rqform:
                    if len(rqform.get(field['FieldName']))!=0:
                        external_uri_list = rqform.get(field['FieldName']).split(',')                     
                elif field['FieldId'] in rqform:
                    if len(rqform.get(field['FieldId']))!=0:
                        external_uri_list = rqform.get(field['FieldId']).split(',')
                

                if len(external_uri_list) > 0:
                    r_item_values,r_rich_values,r_history_values = self.subtract_rich_data(field,external_uri_list,rqurl,current_user.id)
                    item_values.update(r_item_values)
                    rich_values.update(r_rich_values)
                 
            else:



                #Not a rich widget. Will not have rich data
                self.lggr.info(field['FieldName'] +' ('+field['FieldId']+') is NOT a RICH Field ')

                #Form values could be named after FieldName or FieldId, we accept both ways. (second one is more explicit)
                new_raw = ''
                if field['FieldName'] in rqform:
                    if len(rqform.get(field['FieldName']))!=0:
                        new_raw = rqform.get(field['FieldName'])
                elif field['FieldId'] in rqform:
                    if len(rqform.get(field['FieldId']))!=0:
                        new_raw = rqform.get(field['FieldId'])



                if field['FieldType'] == 'OBJECT':
                    try:
                        item_values[field['FieldId']] = json.loads(new_raw.strip())
                    except:
                        item_values[field['FieldId']] = unicode(new_raw).strip()
                else:
                    if new_raw:
                        item_values[field['FieldId']] = unicode(new_raw).strip()
                    else:
                        item_values[field['FieldId']] = None

                            
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

            if 'flag_'+field['FieldName'] in rqform:
                if len(rqform.get('flag_'+field['FieldName']))!=0:
                    flag_values[field['FieldId']] = rqform.get('flag_'+field['FieldName'])
            elif 'flag_'+field['FieldId'] in rqform:
                if len(rqform.get('flag_'+field['FieldId']))!=0:
                    flag_values[field['FieldId']] = rqform.get('flag_'+field['FieldId'])



        RingClass = self.ring_create_class(schema)
        item = RingClass()        
        item._id= str(random.randrange(1000000000,9999999999))
        #item.deleted = 
        item.items.append(**item_values)
        #self.lggr.debug("rich_values:"+str(rich_values))
        #item.rich.append(**rich_values)
        item.rich.append(**rich_values)
        item.history.append(**history_values)
        item.flags.append(**flag_values)
        
        
        if item.store(db):
        
            #Increase item count
            self.increase_item_count(handle,ringname)
            return item._id

        return False


    #AVISPAMODEL
    def get_a_b_c(self,handle,ringname,idx):
        '''
        Gets a specific ring document from DB

        @NOTES: 
          - "human" converts id keys to label keys

        @IN:
          handle = (string)
          ringname = (string)
          idx = (string)
          human = (boolean)

        @OUT:
          ok:(item_doc)
          ko:False

        '''

        self.lggr.debug('++ AVM.get_a_b_c')
        

        schema = self.ring_get_schema_from_view(handle,ringname)   
        OrderedFields=[]
        
        for field in schema['fields']:
            OrderedFields.insert(int(field['FieldOrder']),field['FieldId'])

  

        #self.lggr.debug('select_ring_doc_view(ring/items,'+str(handle)+','+str(ringname)+','+str(idx)+') ')            
        
        result = self.select_ring_doc_view('ring/items',handle,ringname,key=idx)
        
        #self.lggr.debug('result:'+str(result))
        
        for row in result:

            #self.lggr.debug('row:'+str(row))

            #Here i need to convert row keys to Human

            item = self.populate_item(OrderedFields,row)

            #self.lggr.debug(item)

            if item:
                self.lggr.debug('-- AVM.get_a_b_c')
                return item

        #There is no item. It could have been deleted.
        self.lggr.debug('-- AVM.get_a_b_c')
        return False


    #AVISPAMODEL
    def put_a_b_c(self,rqurl,rqform,handle,ringname,idx):
        '''
        Modifies existing document

        @IN:
          rqurl = {(string):(string),}
          rqform = {(string):(string),}
          handle = (string)
          ringname = (string)
          idx = (string)

        @OUT:
          ok:(item_id)
          ko:False

        @COLLATERAL:
          -Overwrites document in DB with modified one


        '''

        self.lggr.info('START AVM.put_a_b_c')

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.MAM.select_db(db_ringname)

        schema = self.ring_get_schema(handle,ringname)
        RingClass = self.ring_create_class(schema)
        item = RingClass.load(db,idx)

        needs_store = False
        
        item_values = {}
        history_values = {}
        rich_values = {}
        fields = schema['fields']

        if rqform.get('_public'):
            item['public']=True
        else:
            item['public']=False

        
        for field in fields:
            
            #VALUES
            new = None
            old = None



            #INITIALIZE FIELD IF IT DOES NOT EXIST
            if field['FieldId'] not in item.items[0]:
                # If it doesn't exist create it
                item.items[0][field['FieldId']] = ''

            #CHECK IF FLAGS EXISTS AND CREATE IT IF NOT
            if 'flags' not in item:
                item['flags'] = []
                item['flags'].append({})


            if field['FieldId'] not in item.flags[0]:
                # If it doesn't exist create it
                item.flags[0][field['FieldId']] = ''

            if field['FieldId'] not in item.history[0]:
                # If it doesn't exist create it
                item.history[0][field['FieldId']] = []

            
            
            if item.items[0][field['FieldId']] == None:
                #Exists in the list but its value is None
                old = None
            else:
                old = item.items[0][field['FieldId']]
            
         
            if field['FieldName'] in rqform:
                if len(rqform.get(field['FieldName']))!=0:
                    new_raw = rqform.get(field['FieldName'])
                else:
                    new_raw = None                   
            elif field['FieldId'] in rqform:
                if len(rqform.get(field['FieldId']))!=0:
                    new_raw = rqform.get(field['FieldId'])
                else:
                    new_raw = None
            else:
                #When a value is expected but not sent 
                new_raw = None

                # i.e: Checkboxes won't send a value if not selected
                '''if field['FieldWidget'] == 'checkbox':
                    new_raw = "false"
                '''


            if field['FieldType'] == 'OBJECT':
                #We need to check if new_raw is a valid json object or just a regular string
                try:
                    new = json.loads(new_raw.strip())
                except:
                    new = ''
                    #new = unicode(new_raw).strip()
            else:
                if new_raw:
                    new = new_raw.strip()
                else:
                    new = None
                   

            if new == '':
               new = None

            if unicode(old) == unicode(new):
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

            old_flag = unicode(item.flags[0][field['FieldId']])

            if 'flag_'+field['FieldName'] in rqform:
                if len(rqform.get('flag_'+field['FieldName']))!=0:
                    new_flag = unicode(rqform.get('flag_'+field['FieldName']))
            elif 'flag_'+field['FieldId'] in rqform:
                if len(rqform.get('flag_'+field['FieldId']))!=0:
                    new_flag = unicode(rqform.get('flag_'+field['FieldId']))
            else:
                new_flag = False

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
                if field['FieldName'] in rqform:
                    if len(rqform.get(field['FieldName']))!=0:
                        external_uri_list = rqform.get(field['FieldName']).split(',')                     
                elif field['FieldId'] in rqform:
                    if len(rqform.get(field['FieldId']))!=0:
                        external_uri_list = rqform.get(field['FieldId']).split(',')
                
                if len(external_uri_list) > 0:
                    r_item_values,r_rich_values,r_history_values = self.subtract_rich_data(
                                                                        field,
                                                                        external_uri_list,
                                                                        rqurl,
                                                                        current_user.id)
                    item_values.update(r_item_values)
                    rich_values.update(r_rich_values)


                    #Repair rich object if needed
                    if 'rich' not in item:
                        self.lggr.debug('REPAIR FLAG 1')
                        #item.rich = []
                        #rich_dict = {}
                        #item.rich.append(rich_dict)
                    elif type(item.rich) is not list:
                        self.lggr.debug('REPAIR FLAG 2')
                        #item.rich = []
                        #rich_dict = {}
                        #item.rich.append(rich_dict)
                    elif type(item.rich[0]) is not dict:
                        self.lggr.debug('REPAIR FLAG 3')
                        #rich_dict = {}
                        #item.rich.append(rich_dict)

                  
                    #1. Save in memory what is in rich data just in case we got a 404
                    old_rich = item.rich[0][field['FieldId']]
                    old_rich_dictionary = {}
                    for old_r in old_rich:
                        if '_source' in old_r:
                            old_rich_dictionary[old_r['_source']] = old_r

                    #self.lggr.debug('old_rich:'+str(old_rich))
                    #self.lggr.debug('old_rich_dictionary:'+str(old_rich_dictionary))

                    #2. Check if we got a 404
                    if field['FieldId'] in r_rich_values:
                        for new_rich_value in r_rich_values[field['FieldId']]:
                            if 'error' in new_rich_value:
                                #3. Check if we can at least have old version (better than nothing)
                                if new_rich_value['_source'] in old_rich_dictionary: 
                                    new_rich_value = old_rich_dictionary[new_rich_value['_source']]

                    if r_rich_values:
                                    
                        item.rich[0][field['FieldId']] = r_rich_values[field['FieldId']]

        self.lggr.info('END AVM.put_a_b_c')

        if needs_store:
            if item.store(db): 
              
                return item._id
        else:
            return item._id

        return False


    def delete_a_b_c(self,handle,ringname,idx):
        '''
        Tombstones item

        @NOTE:
           -It doesn't actually deletes the item from DB it just places a tombstone on it

        @IN:
          handle = (string)
          ringname = (string)
          idx = (string)

        @OUT:
          ok:(item_id)
          ko:False

        @COLLATERAL:
          - Modifies the item in DB

        '''


        db_ringname=str(handle)+'_'+str(ringname)
        db = self.MAM.select_db(db_ringname)

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




    