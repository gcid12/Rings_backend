# AvispaModel.py


from couchdb.http import PreconditionFailed, ResourceNotFound


from datetime import datetime 
import time
import datetime as dt
import random
import sys
import traceback
import collections
from flask import flash
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, ListField, DictField, BooleanField, Mapping 
from couchdb.design import ViewDefinition
from couchdb.http import ResourceNotFound
from MyRingBlueprint import MyRingBlueprint
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
            
            doc = self.MAM.select_user(user_database,handle)
            
            rings = doc['rings']
            
            print(rings)
         

            for ring in rings:
                
                if not 'deleted' in ring:
                    
                    ringname = str(ring['ringname'])+'_'+str(ring['version']) 
                    count = ring['count']
                    print('flag5b:'+str(handle)+'_'+ringname)
                    ringnamedb=str(handle)+'_'+ringname.replace('.','-')
                    print('ringnamedb::'+ringnamedb)
                    db = self.MAM.select_db(ringnamedb)
                    print('Get description:')
                    try:          
                        RingDescription = db['blueprint']['rings'][0]['RingDescription']        
                        r = {'ringname':ringname,'ringdescription':RingDescription,'count':count}
                        data.append(r)
                    except ResourceNotFound:
                        print('skipping ring '+ ringname + '. Blueprint does not exist')
                        

            print('flag6')

            

        except (ResourceNotFound, TypeError) as e:

            #BUG: This exception gets triggered even if the ring does exist
            #The problem has to do with pagination. It can't find it in the current page

            #flash("You have no rings yet, create one!")
            print "Notice: Expected error:", sys.exc_info()[0] , sys.exc_info()[1]
            #print('Notice: No rings for this user.')

        return data


    #AVISPAMODEL
    def ring_set_db(self,handle,ringname,ringversion):
           
        db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
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
    def ring_set_db_views(self,db_ringname):

        db = self.couch[db_ringname]

        
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


        view = ViewDefinition('ring', 'blueprint', 
               '''
                function(doc) {
                  if(doc._id=='blueprint'){   
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
    def user_delete_ring(self,handle,ringname,ringversion,user_database=None):

        db = self.couch[self.user_database]
        doc =  MyRingUser.load(db, handle)
        rings = doc['rings']
        for ring in rings:
            if ring['ringname']==ringname and ring['version']==ringversion:
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

        dbname = handle+'_'+ringname+'_'+ringversion
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
    def ring_get_blueprint(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        print(db_ringname)
        db = self.couch[db_ringname]
        blueprint = MyRingBlueprint.load(db,'blueprint')

        return blueprint



    #AVISPAMODEL
    def ring_set_blueprint(self,handle,ringname,ringversion,pinput,ringprotocol,fieldprotocol):

        
        if ringversion == 'None' or ringversion == None:
            print('ringversion none')
            ringversion = ''

        db_ringname=str(handle)+'_'+str(ringname)+'_'+str(ringversion)
        print('db_ringname:')
        print(db_ringname)
        db = self.couch[db_ringname]
        numfields = len(pinput['fields'])
        ring = MyRingBlueprint.load(db,'blueprint')

        # Creates Ring Blueprint if it doesn't exist. Uses current one if it exists.
        if ring:
            action = 'edit'
        else:       
            ring = MyRingBlueprint()
            #ring = RingClass()
            ring._id= 'blueprint'

            action = 'new'


        # Creates or updates Ring parameters

        args_r = {}
        for r in ringprotocol:
            if(action == 'new'):
                if pinput['rings'][0][r]:
                    args_r[r] = pinput['rings'][0][r]
            
            elif(action == 'edit'):
                if pinput['rings'][0][r] == ring.rings[0][r]:
                    print(r+' did not change')
                    pass
                else:
                    print(r+' changed. Old: "'+ str(ring.rings[0][r]) +'" ('+ str(type(ring.rings[0][r])) +')'+\
                            '  New: "'+ str(pinput['rings'][0][r]) + '" ('+ str(type(pinput['rings'][0][r])) +')' )
                    args_r[r] = pinput['rings'][0][r]

                  

        
        if(action == 'new'):
            ring.rings.append(**args_r)
        
        elif(action == 'edit'):
            for x in args_r:
                ring.rings[0][x] = args_r[x]
            

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
                    if pinput['fields'][i][f] == ring.fields[i][f]:  # Checks if old and new are the same
                        print(f+'_'+str(i+1)+' did not change')
                    else:                      
                        print(f+'_'+str(i+1)+' changed. Old: "'+ str(ring.fields[i][f]) +'" ('+ str(type(ring.fields[i][f])) +')'+\
                            '  New: "'+ str(pinput['fields'][i][f]) + '" ('+ str(type(pinput['fields'][i][f])) +')' )
                        
                        args_f[f] = pinput['fields'][i][f]


            #print('args_f:')
            #print(args_f)

            if(action == 'new'):
                ring.fields.append(**args_f)
                
            elif(action == 'edit'):
                for y in args_f:
                    ring.fields[i][y] = args_f[y]

            args_f={}

        print(ring)

        
        ring.store(db)

        return 'ok'

    
    #AVISPAMODEL
    def _blueprint_create_class(self,numfields,ringprotocol,fieldprotocol):
        '''
        This function is deprecated. Now we just instantiate MyRingBlueprint class
        '''

        args_r = {}
        args_f = {} 

        for r in ringprotocol:

            args_r[r] = TextField()

        for i in xrange(1,numfields):

            for f in fieldprotocol:

                args_f[f] =  TextField()


        blueprintclass = type('BlueprintClass',
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

        return blueprintclass

    
    #AVISPAMODEL
    def ring_create_class(self,blueprint):

        args_i = {}
        fields = blueprint['fields']
        for field in fields:
            args_i[field['FieldName']] = TextField()
 

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
                                                )))
                                               }) 

        return RingClass


    #AVISPAMODEL
    def post_a_b(self,request,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        blueprint = self.ring_get_blueprint(handle,ringname)
        
        values = {}
        fields = blueprint['fields']

        print("post_a_b raw arguments sent:")
        print(request.form)


        for field in fields:
            values[field['FieldName']] = request.form.get(field['FieldName'])

            print(field['FieldName']+' content: '+str(request.form.get(field['FieldName'])))
            print(field['FieldName']+' type: '+str(type(request.form.get(field['FieldName']))))


        RingClass = self.ring_create_class(blueprint)
        item = RingClass()         
        item._id= str(random.randrange(1000000000,9999999999))
        #item.deleted = 
        item.items.append(**values)
        
        if item.store(db):
        
            self.increase_item_count(handle,ringname)

            return item._id

        return False


    #AVISPAMODEL
    def put_a_b_c(self,request,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        blueprint = self.ring_get_blueprint(handle,ringname)
        RingClass = self.ring_create_class(blueprint)
        item = RingClass.load(db,idx)
        
        values = {}
        fields = blueprint['fields']

        if request.form.get('_public'):
            item['public']=True
        else:
            item['public']=False

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

        if item.store(db):      
            return item._id

        return False


    #AVISPAMODEL
    def increase_item_count(self,handle,ringname):

        self.db = self.couch[self.user_database]
        user =  MyRingUser.load(self.db, handle)

        if user:

            for ring in user['rings']:
                if ring['ringname']+'_'+ring['version'] == ringname:
                    ring['count'] += 1
                    print('Item Count increased')

            if user.store(self.db):
                
                return True
            else:
                print('Could not increase item count')
                return False


    #AVISPAMODEL
    def get_a_b(self,handle,ringname,limit=100,lastkey=None):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]
        batch = 500  #This is not the number of results per page. 
         # https://pythonhosted.org/CouchDB/client.html#couchdb.client.Database.iterview

        blueprint = self.ring_get_blueprint_from_view(handle,ringname) 
        OrderedFields=[]
        for field in blueprint['fields']:
            OrderedFields.insert(int(field['FieldOrder']),field['FieldName'])
            

        #print('blueprint:')
        #print(blueprint)

        print('OrderedFields:')
        print(OrderedFields)

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

        #print (result)
        items = []
        i = 0

        for row in result:

            i += 1
            if lastkey and i==1:
                #If lastkey was sent, ignore first item 
                #as it was the last item in the last page
                print('length:')
                print(len(items))
                continue
                #pass

            #item = {} #Make this an ordered dictionary
            item = collections.OrderedDict()

            item[u'_id'] = row['id']

            for fieldname in OrderedFields:
                item[fieldname] = row['value'][fieldname]

            #item.update(row['value'])

            #item['id']=row['id']
            #item['values']=row['value']
            items.append(item)
            print("item:")
            print(item)

        #print(items)

        return items


    #AVISPAMODEL
    def get_a_b_c(self,request,handle,ringname,idx):

        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        blueprint = self.ring_get_blueprint_from_view(handle,ringname)   
        OrderedFields=[]
        for field in blueprint['fields']:
            print("order:FieldName")
            print(field['FieldOrder'],field['FieldName'])
            OrderedFields.insert(int(field['FieldOrder']),field['FieldName'])
            print(OrderedFields)

        
        options = {}
        options['key']=idx

        #Retrieving from ring/items view
        result = db.iterview('ring/items',1,**options)

        
        for row in result:      
            item = collections.OrderedDict()
            if row['id']:        
                item[u'_id'] = row['id']

                for fieldname in OrderedFields:
                    item[fieldname] = row['value'][fieldname]
                    #item.update(row['value'])

                print("item:")
                return item

        return False

    #AVISPAMODEL
    def ring_get_blueprint_from_view(self,handle,ringname):

        db_ringname=str(handle)+'_'+str(ringname)
        print(db_ringname)
        db = self.couch[db_ringname]

        options = {}
        result  = db.iterview('ring/blueprint',1,**options)

        for row in result:  
            #print('row.value.fields:')
            #print(row.value['fields'])    
            blueprint = {}
            #blueprint['rings']=row.value
            blueprint['fields']=row.value['fields']
            blueprint['rings']=row.value['rings']
            #blueprint['rings']=row.rings
            #blueprint['fields']=row.fields

        #print('blueprint:')
        #print(blueprint)

        return blueprint

        #return False
        


        ''' Optional way to retrieve from DB (not view)

        blueprint = self.ring_get_blueprint(handle,ringname)
        RingClass = self.ring_create_class(blueprint)

        item = RingClass.load(db,idx)
        item['items'][0][u'id']=idx


        #return item['items'][0]
        '''

    def delete_a_b_c(self,request,handle,ringname,idx):


        db_ringname=str(handle)+'_'+str(ringname)
        db = self.couch[db_ringname]

        blueprint = self.ring_get_blueprint(handle,ringname)
        RingClass = self.ring_create_class(blueprint)
        item = RingClass.load(db,idx)
        
        '''
        values = {}
        fields = blueprint['fields']
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

    